import socket
import time
import requests
import subprocess
from datetime import datetime

HOSTNAME = socket.gethostname()

def get_open_http_ports():
    ports = set()
    try:
        result = subprocess.run(["ss", "-tln"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "LISTEN" in line:
                parts = line.split()
                address = parts[-1]
                if ':' in address:
                    port_str = address.split(":")[-1]
                    if port_str.isdigit():
                        port = int(port_str)
                        if 80 <= port <= 9000:
                            ports.add(port)
    except Exception as e:
        print(f"❌ Error scanning ports: {e}")
    return sorted(ports)

def is_web_app(port):
    try:
        response = requests.get(f"http://localhost:{port}", timeout=2)
        return response.status_code < 600
    except Exception:
        return False

def collect_web_apm(port):
    try:
        start = time.time()
        response = requests.get(f"http://localhost:{port}", timeout=2)
        latency_ms = round((time.time() - start) * 1000, 2)
        return {
            "Request Count": 1,
            "Avg Response Time (ms)": latency_ms,
            "Status Code": response.status_code
        }
    except Exception as e:
        return {
            "Request Count": 1,
            "Avg Response Time (ms)": None,
            "Error": str(e)
        }

def run_once():
    open_ports = get_open_http_ports()
    print(f"🔍 Detected open ports: {open_ports}")

    metrics = {}
    for port in open_ports:
        if is_web_app(port):
            apm = collect_web_apm(port)
            app_key = f"app_on_port_{port}"
            metrics[app_key] = apm

    if not metrics:
        print(f"[{datetime.now()}] ⚠️ No web applications detected.")
    else:
        print(f"[{datetime.now()}] ✅ Web APM metrics:")
        for app, apm in metrics.items():
            print(f"  {app}: {apm}")

if __name__ == "__main__":
    run_once()
