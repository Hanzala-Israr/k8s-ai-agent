import os
from kubernetes import client, config

def init_k8s():
    # Attempt to load kubeconfig from default location or KUBECONFIG env var
    try:
        config.load_kube_config()
        print("✅ [INFO] Loaded local kubeconfig successfully.")
    except Exception as e:
        print(f"❌ [ERROR] Could not load kubeconfig: {e}")
        return None
    
    return client.CoreV1Api()

def test_connectivity(v1):
    if not v1: return
    try:
        # Fetching nodes to confirm cluster access
        nodes = v1.list_node()
        print(f"🚀 [SUCCESS] Cluster connection active! Nodes detected: {len(nodes.items)}")
        for node in nodes.items:
            print(f"  • Node: {node.metadata.name}")
    except Exception as e:
        print(f"❌ [ERROR] API call failed: {e}")

if __name__ == "__main__":
    v1_api = init_k8s()
    test_connectivity(v1_api)
