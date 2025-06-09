import psutil
import requests
import time
import socket
import os
import json
from datetime import datetime

HOSTNAME = socket.gethostname()
API_ENDPOINT = os.getenv("APM_SERVER_ENDPOINT", "http://52.170.6.111:8030/metrics/upload")  # Azure endpoint

def get_server_apm(pid):
    try:
        proc = psutil.Process(pid)
        with proc.oneshot():
            cpu = proc.cpu_percent(interval=1)
            mem = proc.memory_info().rss / (1024 ** 2)
            create_time = datetime.fromtimestamp(proc.create_time()).strftime("%Y-%m-%d %H:%M:%S")
        return {
            "CPU (%)": round(cpu, 2),
            "Memory (MB)": round(mem, 2),
            "Uptime Since": create_time
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return {
            "CPU (%)": -1,
            "Memory (MB)": -1,
            "Uptime Since": "N/A"
        }

def collect_and_push_server_apm():
    while True:
        metrics = {}
        seen = set()

        for conn in psutil.net_connections(kind="inet"):
            if conn.status == psutil.CONN_LISTEN:
                pid = conn.pid
                port = conn.laddr.port

                if pid and port and (pid, port) not in seen:
                    seen.add((pid, port))
                    try:
                        app_key = f"app_on_port_{port}"
                        metrics[app_key] = {"server_apm": get_server_apm(pid)}
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

        payload = {
            "hostname": HOSTNAME,
            "metrics": metrics
        }

        try:
            print(f"📦 Sending Server APM payload: {json.dumps(payload, indent=2)}")
            res = requests.post(API_ENDPOINT, json=payload)
            print(f"[{datetime.now()}] ✅ Server APM pushed: {res.status_code}", flush=True)
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Failed to push Server APM: {e}", flush=True)

        time.sleep(60)

if __name__ == "__main__":
    collect_and_push_server_apm()
