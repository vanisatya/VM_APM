import psutil
import requests
import time
import socket
import os
from datetime import datetime

API_ENDPOINT = "https://vm-apm.onrender.com/metrics/upload"
HOSTNAME = socket.gethostname()

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
        apm = {}
        seen = set()

        for conn in psutil.net_connections(kind="inet"):
            if conn.status == psutil.CONN_LISTEN:
                pid = conn.pid
                port = conn.laddr.port

                if pid and port and (pid, port) not in seen:
                    seen.add((pid, port))
                    try:
                        proc_name = psutil.Process(pid).name()
                        key = f"{HOSTNAME}::{proc_name}:{port}"
                        apm[key] = {"server_apm": get_server_apm(pid)}
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue

        try:
            res = requests.post(API_ENDPOINT, json=apm)
            print(f"[{datetime.now()}] ✅ Server APM pushed: {res.status_code}", flush=True)
        except Exception as e:
            print(f"[{datetime.now()}] ❌ Failed to push Server APM: {e}", flush=True)

        time.sleep(60)

if __name__ == "__main__":
    collect_and_push_server_apm()