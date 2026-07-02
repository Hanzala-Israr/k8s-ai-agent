# 🚀 AI-Powered Kubernetes Troubleshooting Agent

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi)
![Kubernetes](https://img.shields.io/badge/Kubernetes-KinD-326CE5?style=for-the-badge&logo=kubernetes)
![Gemini](https://img.shields.io/badge/Google-Gemini_2.5_Flash-4285F4?style=for-the-badge&logo=google)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite)

</p>

An **AI-powered Site Reliability Engineering (SRE) platform** that continuously scans Kubernetes namespaces, detects unhealthy workloads, gathers runtime telemetry (logs, events, pod metadata), and leverages **Google Gemini 2.5 Flash** to perform automated root cause analysis and generate structured remediation recommendations.

Designed as a complete full-stack DevOps project, the platform combines Kubernetes automation, FastAPI, Generative AI, SQLite persistence, and an interactive web dashboard into a single troubleshooting system.

---

# 🎥 Demo Video

> **Demo Video:**




https://github.com/user-attachments/assets/14f7c6ae-6781-4222-85e8-2fe86cfbf984




---

# 📸 Screenshots

| Dashboard |
|-----------|
| <img width="1600" height="1232" alt="WhatsApp Image 2026-07-02 at 11 49 20 AM" src="https://github.com/user-attachments/assets/1404732b-c0ae-4ae1-bdc5-85129106bb5f" />
 

---

# ✨ Features

- 🔍 Automated Kubernetes namespace inspection
- 🤖 AI-powered root cause analysis using Google Gemini 2.5 Flash
- 📄 Collects pod logs, events, and runtime metadata
- ⚡ Detects unhealthy workloads automatically
- 📊 Interactive monitoring dashboard
- 💾 SQLite investigation history
- 🔄 FastAPI asynchronous REST API
- 📦 JSON structured AI responses using Pydantic schemas
- 🛠 Generates practical remediation commands
- 📈 Maintains complete investigation history

---

# 🏗️ System Architecture

```text
                     Kubernetes Cluster
              (KinD / Pods / Events / Logs)
                           │
                           ▼
             ┌────────────────────────────┐
             │ Kubernetes Inspector Layer │
             │  • Pod Scanner             │
             │  • Log Collector           │
             │  • Event Collector         │
             └────────────────────────────┘
                           │
                           ▼
             ┌────────────────────────────┐
             │     FastAPI Backend        │
             │  Investigation Pipeline    │
             └────────────────────────────┘
                           │
                           ▼
             ┌────────────────────────────┐
             │ Google Gemini 2.5 Flash AI │
             │ Structured Incident Report │
             └────────────────────────────┘
                           │
                 ┌─────────┴─────────┐
                 ▼                   ▼
          SQLite Database      Web Dashboard
```

---

# ⚙️ Tech Stack

| Category | Technology |
|----------|------------|
| Language | Python 3.10+ |
| Backend | FastAPI |
| Server | Uvicorn |
| AI | Google Gemini 2.5 Flash |
| SDK | google-genai |
| Infrastructure | Kubernetes (KinD) |
| Kubernetes SDK | Official Kubernetes Python Client |
| Database | SQLite |
| Frontend | HTML5, Tailwind CSS, JavaScript |
| API Validation | Pydantic |

---

# 📂 Project Structure

```text
k8s-ai-agent/
│
├── backend/
│   ├── agent.py
│   ├── database.py
│   ├── history.db
│   ├── inspector.py
│   ├── main.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
│
├── broken-app.yaml
├── README.md
└── venv/
```

---

# 🔄 Investigation Workflow

```text
User
 │
 ▼
Dashboard
 │
 ▼
FastAPI API
 │
 ▼
Kubernetes Inspector
 │
 ├── Scan Pods
 ├── Fetch Logs
 └── Collect Events
 │
 ▼
Gemini AI
 │
 ▼
Root Cause Analysis
 │
 ▼
SQLite Database
 │
 ▼
Dashboard Visualization
```

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/k8s-ai-agent.git

cd k8s-ai-agent
```

---

## 2. Create Virtual Environment

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r backend/requirements.txt
```

---

## 4. Create Kubernetes Cluster

```bash
kind create cluster --name troubleshooting-matrix
```

Verify:

```bash
kubectl get nodes
```

---

## 5. Configure Gemini API Key

Generate an API key from **Google AI Studio**.

Export it:

```bash
export GEMINI_API_KEY="YOUR_API_KEY"
```

Verify:

```bash
echo $GEMINI_API_KEY
```

---

## 6. Start Backend

```bash
cd backend

python main.py
```

or

```bash
uvicorn main:app --reload
```

---

## 7. Open Dashboard

```
http://YOUR_EC2_PUBLIC_IP:8000
```

---

# 🧪 Testing the AI Agent

Deploy a broken workload.

Example:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-processor-service

spec:
  replicas: 1

  selector:
    matchLabels:
      app: payment-processor

  template:
    metadata:
      labels:
        app: payment-processor

    spec:
      containers:
      - name: payment-api

        image: nginx:alpine-v99.32.12
```

Deploy it:

```bash
kubectl apply -f broken-app.yaml
```

Click

```
Analyze Cluster State
```

The platform automatically:

- Detects ImagePullBackOff
- Retrieves Events
- Retrieves Pod Logs
- Sends evidence to Gemini
- Generates AI remediation
- Saves investigation to SQLite

---

# 📋 Failure Modes Supported

The platform currently diagnoses:

- ✅ CrashLoopBackOff
- ✅ ImagePullBackOff
- ✅ CreateContainerConfigError
- ✅ Missing Environment Variables
- ✅ Missing Secrets
- ✅ Missing ConfigMaps
- ✅ OOMKilled Containers
- ✅ Scheduling Failures
- ✅ Liveness Probe Failures
- ✅ Readiness Probe Failures
- ✅ Container Exit Code Failures

---

# 📊 API Endpoints

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/` | Dashboard UI |
| GET | `/api/health` | Health Check |
| GET | `/api/history` | Investigation History |
| POST | `/api/investigate` | Trigger AI Investigation |

---

# 💡 Example AI Response

```json
{
  "status": "anomaly_detected",
  "analysis": {
    "incident_summary": "Container failed to start.",
    "root_cause": "ImagePullBackOff caused by an invalid image tag.",
    "confidence_score": 98,
    "suggested_fix": "kubectl set image deployment/payment-processor-service payment-api=nginx:alpine",
    "prevention_strategy": "Use immutable image tags and CI validation."
  }
}
```

# 👨‍💻 Author

**Hanzala Israr**
