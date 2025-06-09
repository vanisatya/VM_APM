import psutil
import requests
import time
import socket
import os
import json
from datetime import datetime

HOSTNAME = socket.gethostname()
API_ENDPOINT = os.getenv("APM_SERVER_ENDPOINT", "http://52.170.6.111:8030/metrics/upload")

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

        # First collect for processes with open ports
        for conn in psutil.net_connections(kind="inet"):
            if conn.status == psutil.CONN_LISTEN:
                pid = conn.pid
                port = conn.laddr.port
                if pid and port and (pid, port) not in seen:
                    seen.add((pid, port))
                    metrics[f"app_on_port_{port}"] = {"server_apm": get_server_apm(pid)}

        # Then collect for all other top-level processes (not already captured)
        for proc in psutil.process_iter(['pid', 'name']):
            pid = proc.info['pid']
            name = proc.info['name']
            if all(pid != s[0] for s in seen):
                key = f"proc_{pid}_{name}"
                metrics[key] = {"server_apm": get_server_apm(pid)}

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
