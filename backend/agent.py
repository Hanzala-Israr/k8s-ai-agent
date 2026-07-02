import os
import json
from google import genai
from google.genai import types


class K8sAIAgent:
    def __init__(self):
        """
        Initializes the unified Google GenAI client.
        """
        # The Client automatically extracts the GEMINI_API_KEY environment variable
        if not os.environ.get("GEMINI_API_KEY"):
            raise ValueError(
                "❌ [CRITICAL]: GEMINI_API_KEY environment variable is missing."
            )

        self.client = genai.Client()

        # Using Gemini 2.5 Flash for fast inference
        self.model_name = "gemini-2.5-flash"

    def _build_troubleshooting_prompt(
        self,
        pod_signals: list,
        logs: str,
        events: list,
    ) -> str:
        """
        Converts raw unstructured cluster signals into a highly structured
        markdown evidence dossier for deep LLM contextual reasoning.
        """

        prompt = f"""
### KUBERNETES INCIDENT EVIDENCE DOSSIER

[1. TARGET POD METADATA SIGNALS]
{json.dumps(pod_signals, indent=2) if pod_signals else "No active pod telemetry metrics."}

[2. LIVE CONTROL PLANE EVENT WARNINGS]
{json.dumps(events, indent=2) if events else "No active cluster hardware or scheduling warnings found."}

[3. TERMINAL LOG EXCERPT (STDERR/STDOUT)]

```text
{logs if logs else "No execution runtime log dumps available."}
```
"""

        return prompt

    def analyze_incident(
        self,
        pod_signals: list,
        logs: str,
        events: list,
    ) -> dict:
        """
        Executes reasoning over cluster metrics and returns a strictly typed
        JSON schema report pinpointing root cause analysis and remedies.
        """

        raw_prompt = self._build_troubleshooting_prompt(
            pod_signals,
            logs,
            events,
        )

        system_instruction = (
            "You are an expert Principal Site Reliability Engineer (SRE) "
            "and Kubernetes core developer. "
            "Your task is to analyze the provided cluster metrics, events, "
            "and log anomalies to identify the true root cause. "
            "Be definitive, trace misconfigurations accurately, and provide "
            "practical, direct terminal remediation scripts."
        )

        json_schema = {
            "type": "OBJECT",
            "properties": {
                "incident_summary": {
                    "type": "STRING"
                },
                "root_cause": {
                    "type": "STRING"
                },
                "confidence_score": {
                    "type": "INTEGER"
                },
                "suggested_fix": {
                    "type": "STRING"
                },
                "prevention_strategy": {
                    "type": "STRING"
                },
            },
            "required": [
                "incident_summary",
                "root_cause",
                "confidence_score",
                "suggested_fix",
                "prevention_strategy",
            ],
        }

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=raw_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    response_mime_type="application/json",
                    response_schema=json_schema,
                    temperature=0.1,
                ),
            )

            return json.loads(response.text)

        except Exception as e:
            return {
                "incident_summary": "Failed to compile automated analysis.",
                "root_cause": f"AI Reasoning Engine error context: {str(e)}",
                "confidence_score": 0,
                "suggested_fix": (
                    "Inspect backend engine configuration and API billing parameters."
                ),
                "prevention_strategy": "N/A",
            }


if __name__ == "__main__":
    # Smoke-test run verifying API loop and schema verification

    print("🧠 Initializing AI Reasoning Grid...")

    agent = K8sAIAgent()

    # Mock parameters simulating a typical database connection string absence failure
    mock_pod = [
        {
            "pod_name": "api-worker-pod",
            "phase": "Failed",
            "reason": "Error",
            "message": "Exit code 1",
        }
    ]

    mock_logs = (
        "FATAL: Connection failed to database at postgres://localhost:5432. "
        "Environment variable 'DATABASE_URL' is undefined."
    )

    mock_events = [
        {
            "type": "Warning",
            "reason": "BackOff",
            "message": "Back-off restarting failed container",
        }
    ]

    print("⚡ Sending mock dossier to Gemini Platform...")

    analysis = agent.analyze_incident(
        mock_pod,
        mock_logs,
        mock_events,
    )

    print("\n📋 [AI ANALYSIS RETURNED STRUCTURALLY SUCCESSFUL]:")

    print(json.dumps(analysis, indent=2))
