import sqlite3
import json
import os

DB_PATH = os.path.expanduser("~/k8s-ai-agent/backend/history.db")

def init_db():
    """Initializes the SQLite database and creates the history table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS investigations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            namespace TEXT NOT NULL,
            status TEXT NOT NULL,
            target_pod TEXT,
            analysis_json TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print("💾 [DATABASE MANAGER]: History log schema verified/initialized.")

def save_investigation(namespace: str, status: str, target_pod: str, analysis: dict):
    """Persists a snapshot of the investigation telemetry and AI results."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO investigations (namespace, status, target_pod, analysis_json)
        VALUES (?, ?, ?, ?)
    """, (namespace, status, target_pod, json.dumps(analysis)))
    conn.commit()
    conn.close()

def get_history():
    """Retrieves all past cluster analysis items formatted for frontend display."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, timestamp, namespace, status, target_pod, analysis_json FROM investigations ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    history_list = []
    for row in rows:
        history_list.append({
            "id": row[0],
            "timestamp": row[1],
            "namespace": row[2],
            "status": row[3],
            "target_pod": row[4] or "N/A",
            "analysis": json.loads(row[5])
        })
    return history_list
