from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn

from inspector import K8sInspector
from agent import K8sAIAgent
import database


app = FastAPI(
    title="AI Kubernetes Troubleshooting Control Plane",
    version="1.0.0",
)

# ----------------------------------------------------------
# Enable CORS
# ----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------
# Initialize Database
# ----------------------------------------------------------
database.init_db()

# ----------------------------------------------------------
# Initialize Core Components
# ----------------------------------------------------------
try:
    inspector = K8sInspector()
    ai_agent = K8sAIAgent()

except Exception as e:
    print(f"❌ [CRITICAL ENGINE FAILURE]: {e}")
    inspector = None
    ai_agent = None


# ----------------------------------------------------------
# Serve Frontend Dashboard
# ----------------------------------------------------------
@app.get("/")
def serve_dashboard():
    """
    Serves the graphical SRE dashboard.
    """
    project_root = Path(__file__).resolve().parent.parent
    html_path = project_root / "frontend" / "index.html"

    return FileResponse(html_path)


# ----------------------------------------------------------
# Request Model
# ----------------------------------------------------------
class InvestigationRequest(BaseModel):
    namespace: str = "default"


# ----------------------------------------------------------
# Health Endpoint
# ----------------------------------------------------------
@app.get("/api/health")
def health_check():
    return {
        "status": "healthy"
    }


# ----------------------------------------------------------
# Investigation History
# ----------------------------------------------------------
@app.get("/api/history")
def fetch_history():
    return database.get_history()


# ----------------------------------------------------------
# Investigation Endpoint
# ----------------------------------------------------------
@app.post("/api/investigate")
async def trigger_investigation(request: InvestigationRequest):

    if inspector is None or ai_agent is None:
        raise HTTPException(
            status_code=503,
            detail="System engines are offline."
        )

    try:

        unhealthy_pods = inspector.scan_unhealthy_pods(
            namespace=request.namespace
        )

        # --------------------------------------------------
        # Healthy Namespace
        # --------------------------------------------------
        if not unhealthy_pods:

            response_payload = {
                "status": "clean",
                "message": f"All workloads in namespace '{request.namespace}' are reporting healthy.",
                "analysis": {
                    "incident_summary": "Namespace is completely healthy.",
                    "root_cause": "No anomalies or failed pods detected.",
                    "confidence_score": 100,
                    "suggested_fix": "No action required.",
                    "prevention_strategy": "Maintain active health monitoring probes."
                }
            }

            database.save_investigation(
                namespace=request.namespace,
                status="clean",
                target_pod=None,
                analysis=response_payload["analysis"]
            )

            return response_payload

        # --------------------------------------------------
        # Investigate First Unhealthy Pod
        # --------------------------------------------------
        target_pod = unhealthy_pods[0]

        pod_name = target_pod["pod_name"]
        container_name = target_pod["container_name"]

        pod_logs = inspector.fetch_pod_logs(
            pod_name=pod_name,
            container_name=container_name,
            namespace=request.namespace
        )

        cluster_events = inspector.gather_cluster_events(
            pod_name=pod_name,
            namespace=request.namespace
        )

        ai_analysis = ai_agent.analyze_incident(
            pod_signals=[target_pod],
            logs=pod_logs,
            events=cluster_events
        )

        response_payload = {
            "status": "anomaly_detected",
            "investigated_target": {
                "pod": pod_name,
                "container": container_name,
                "phase": target_pod["phase"]
            },
            "analysis": ai_analysis
        }

        database.save_investigation(
            namespace=request.namespace,
            status="anomaly_detected",
            target_pod=pod_name,
            analysis=ai_analysis
        )

        return response_payload

    except Exception as e:

        print(f"❌ [BACKEND ERROR]: {e}")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ----------------------------------------------------------
# Launch Server
# ----------------------------------------------------------
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
