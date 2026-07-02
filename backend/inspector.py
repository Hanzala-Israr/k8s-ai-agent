import sys
from kubernetes import client, config
from kubernetes.client.rest import ApiException

class K8sInspector:
    def __init__(self):
        """Initializes client configurations for cluster hooks."""
        try:
            config.load_kube_config()
            self.v1 = client.CoreV1Api()
            self.apps_v1 = client.AppsV1Api()
        except Exception as e:
            print(f"❌ [INSPECTOR INITIALIZATION FAILED]: {e}")
            sys.exit(1)

    def scan_unhealthy_pods(self, namespace: str = "default"):
        """
        Layer 1: Pod Inspector
        Scans a namespace and aggregates precise state signals for any non-Running pods.
        """
        unhealthy_signals = []
        try:
            pods = self.v1.list_namespaced_pod(namespace=namespace)
            for pod in pods.items:
                pod_name = pod.metadata.name
                phase = pod.status.phase
                
                # Check container statuses for discrete failure states (CrashLoopBackOff, ImagePullBackOff)
                container_statuses = pod.status.container_statuses or []
                for status in container_statuses:
                    container_name = status.name
                    ready = status.ready
                    restart_count = status.restart_count
                    
                    # Dig into waiting states to catch the real K8s abstraction reason code
                    state_reason = "None"
                    state_message = "None"
                    if status.state.waiting:
                        state_reason = status.state.waiting.reason
                        state_message = status.state.waiting.message
                    elif status.state.terminated:
                        state_reason = status.state.terminated.reason
                        state_message = status.state.terminated.message

                    # Flag anything that is not ready or in a Failed/Pending phase
                    if not ready or phase in ["Failed", "Pending"]:
                        unhealthy_signals.append({
                            "pod_name": pod_name,
                            "container_name": container_name,
                            "phase": phase,
                            "restart_count": restart_count,
                            "reason": state_reason,
                            "message": state_message
                        })
            return unhealthy_signals
        except ApiException as e:
            print(f"❌ Error fetching pods: {e}")
            return []

    def fetch_pod_logs(self, pod_name: str, container_name: str, namespace: str = "default", lines: int = 40):
        """
        Layer 2: Logs Collector
        Fetches container execution dumps. If a container has crashed repeatedly,
        it automatically extracts the logs from the previous execution loop.
        """
        try:
            # First attempt to read current execution stream logs
            return self.v1.read_namespaced_pod_log(
                name=pod_name,
                container=container_name,
                namespace=namespace,
                tail_lines=lines
            )
        except ApiException as e:
            # If the container is dead/restarting, fall back to capturing its previous crashed state logs
            try:
                return self.v1.read_namespaced_pod_log(
                    name=pod_name,
                    container=container_name,
                    namespace=namespace,
                    tail_lines=lines,
                    previous=True
                )
            except ApiException as prev_err:
                return f"⚠️ Could not pull stdout/stderr data. Logs status: {prev_err.reason}"

    def gather_cluster_events(self, pod_name: str, namespace: str = "default"):
        """
        Layer 3: Events Analyzer
        Queries the namespace control plane for structural infrastructure failure warnings
        specifically mapped to the targeted resource UID.
        """
        event_logs = []
        try:
            # Filter cluster-wide events specifically referencing our target resource name
            field_selector = f"involvedObject.name={pod_name}"
            events = self.v1.list_namespaced_event(namespace=namespace, field_selector=field_selector)
            
            for event in events.items:
                # Capture Warnings like FailedScheduling, FailedMount, BackOff, etc.
                event_logs.append({
                    "type": event.type,
                    "reason": event.reason,
                    "message": event.message,
                    "count": event.count
                })
            return event_logs
        except ApiException as e:
            print(f"❌ Error scraping events: {e}")
            return []

if __name__ == "__main__":
    # Smoke test verification loop
    inspector = K8sInspector()
    print("🔬 Running internal diagnostic collection check...")
    test_scan = inspector.scan_unhealthy_pods(namespace="default")
    print(f"📋 Current Unhealthy Pod Array: {test_scan}")
