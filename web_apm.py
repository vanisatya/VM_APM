import socket
import time
import requests
import subprocess
import json
from datetime import datetime

API_ENDPOINT = "https://vm-apm.onrender.com/metrics/upload"
HOSTNAME = socket.gethostname()


def get_open_http_ports():
    """Scan all TCP listening ports and identify HTTP servers"""
    ports = set()
    try:
        # Run 'ss' to get all listening TCP ports
        result = subprocess.run(["ss", "-tln"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "LISTEN" in line:
                parts = line.split()
                address = parts[-1]
                if ':' in address:
                    port_str = address.split(":")[-1]
                    if port_str.isdigit():
                        port = int(port_str)
                        # Limit to common web port range
                        if 80 <= port <= 9000:
                            ports.add(port)
    except Exception as e:
        print(f"❌ Error while scanning ports: {e}")
    return sorted(ports)


def is_web_app(port):
    """Check if the given port responds to HTTP GET request"""
    try:
        response = requests.get(f"http://localhost:{port}", timeout=2)
        return response.status_code < 600
    except Exception:
        return False


def collect_web_apm(port):
    """Collect response time and status code for a single port"""
    try:
        start = time.time()
        response = requests.get(f"http://localhost:{port}", timeout=2)
        end = time.time()

        latency_ms = round((end - start) * 1000, 2)

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


def push_metrics():
    open_ports = get_open_http_ports()
    payload = {}

    for port in open_ports:
        if is_web_app(port):
            apm = collect_web_apm(port)
            app_key = f"app_on_port_{port}"
            payload[app_key] = {"web_apm": apm}

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
