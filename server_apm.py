import psutil
import requests
import socket
import time
import json
import os
from datetime import datetime
import subprocess

HOSTNAME = socket.gethostname()
API_ENDPOINT = os.getenv("APM_SERVER_ENDPOINT", "http://52.170.6.111:8030/metrics/upload")

def get_open_http_ports():
    ports = set()
    try:
        result = subprocess.run(["ss", "-tln"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "LISTEN" not in line:
                continue
            parts = line.split()
            for part in parts:
                if ':' in part:
                    try:
                        port = int(part.rsplit(":", 1)[-1])
                        if 1 <= port <= 65535:
                            ports.add(port)
                    except ValueError:
                        continue
    except Exception as e:
        print(f"❌ Error scanning ports: {e}")
    return sorted(ports)

def get_pid_for_port(port):
    try:
        for conn in psutil.net_connections(kind="inet"):
            if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port and conn.pid:
                return conn.pid
    except Exception:
        return None
    return None

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

def run_once():
    ports = get_open_http_ports()
    print(f"🔍 Detected open ports: {ports}")
    metrics = {}

    for port in ports:
        pid = get_pid_for_port(port)
        if pid:
            key = f"app_on_port_{port}"
            metrics[key] = {"server_apm": get_server_apm(pid)}

    if not metrics:
        print(f"[{datetime.now()}] ⚠️ No web applications detected.")
    else:
        payload
