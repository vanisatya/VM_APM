import os
import json
import time
import socket
import requests
from collections import defaultdict
from datetime import datetime

API_ENDPOINT = "https://vm-apm.onrender.com/metrics/upload"
HOSTNAME = socket.gethostname()
PARENT_DIR = "/home"  # Works across all VMs

def discover_apps(base_dir):
    apps = []
    for user_dir in os.listdir(base_dir):
        user_path = os.path.join(base_dir, user_dir)
        if os.path.isdir(user_path):
            for app in os.listdir(user_path):
                app_path = os.path.join(user_path, app)
                logs_path = os.path.join(app_path, "logs", "web_apm.log")
                if os.path.isfile(logs_path):
                    apps.append((app, logs_path))
    return apps

def summarize_web_apm(log_path):
    try:
        with open(log_path, 'r') as f:
            logs = [json.loads(line) for line in f.readlines()[-200:] if '"type": "web_apm"' in line]
        if not logs:
            return {}

        total_requests = len(logs)
        avg_response_time = sum(log.get("response_time_ms", 0) for log in logs) / total_requests

        return {
            "Request Count": total_requests,
            "Avg Response Time (ms)": round(avg_response_time, 2)
        }
    except Exception as e:
        print(f"❌ Error reading {log_path}: {e}")
        return {}

def push_metrics():
    payload = {}
    for app_name, log_path in discover_apps(PARENT_DIR):
        web_metrics = summarize_web_apm(log_path)
        if web_metrics:
            payload[app_name] = {"web_apm": web_metrics}

    print(f"📦 Sending Web APM payload: {json.dumps(payload)}")
    try:
        res = requests.post(API_ENDPOINT, json={"hostname": HOSTNAME, "metrics": payload})
        print(f"[{datetime.now()}] ✅ Web APM pushed: {res.status_code}")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Failed to push Web APM: {e}")

if __name__ == "__main__":
    while True:
        push_metrics()
        time.sleep(60)
