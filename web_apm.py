import os
import json
import time
import requests
import socket
from datetime import datetime

API_ENDPOINT = os.getenv("API_ENDPOINT", "https://your-render-app.onrender.com/metrics/upload")
HOSTNAME = socket.gethostname()
PARENT_DIR = os.getenv("APPS_BASE_DIR", "/")  # default to root if unspecified

def discover_apps(base_dir):
    apps = []
    for root, dirs, files in os.walk(base_dir):
        if "logs" in dirs:
            log_path = os.path.join(root, "logs", "access.log")
            if os.path.isfile(log_path):
                app_name = os.path.basename(os.path.dirname(root))
                apps.append((f"{HOSTNAME}::{app_name}", log_path))
    return apps

def summarize_web_apm(log_path):
    try:
        with open(log_path) as f:
            logs = [json.loads(line) for line in f.readlines()[-200:] if '"type": "web_apm"' in line]
        if not logs:
            return {}
        count = len(logs)
        avg_resp_time = sum(log.get("response_time", 0) for log in logs) / count
        return {
            "Request Count": count,
            "Avg Response Time (ms)": round(avg_resp_time, 2)
        }
    except Exception as e:
        return {}

def collect_and_push_web_apm():
    while True:
        apps = discover_apps(PARENT_DIR)
        payload = {}

        for app_id, log_path in apps:
            web_metrics = summarize_web_apm(log_path)
            if web_metrics:
                payload[app_id] = {"web_apm": web_metrics}

        try:
            requests.post(API_ENDPOINT, json=payload)
            print(f"[{datetime.now()}] ✅ Web APM pushed")
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Failed to push web APM:", e)

        time.sleep(60)

if __name__ == "__main__":
    collect_and_push_web_apm()
