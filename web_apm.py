import socket
import requests
import psutil
import time

def discover_web_apps():
    apps = []
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port in (80, 443) or conn.laddr.port >= 8000:
            pid = conn.pid
            if pid:
                try:
                    proc = psutil.Process(pid)
                    name = proc.name()
                    apps.append({
                        "port": conn.laddr.port,
                        "pid": pid,
                        "name": name,
                        "url": f"http://localhost:{conn.laddr.port}"
                    })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
    return apps

def get_web_apm(app):
    try:
        start = time.time()
        res = requests.get(app["url"], timeout=2)
        duration = (time.time() - start) * 1000  # ms
        return {
            "Request Count": 1,  # In real use, count over time
            "Avg Response Time (ms)": round(duration, 2),
            "Status Code": res.status_code
        }
    except Exception:
        return {
            "Request Count": 1,
            "Avg Response Time (ms)": -1,
            "Status Code": "Error"
        }

def collect_all_web_apm():
    apps = discover_web_apps()
    apm_data = {}
    for app in apps:
        apm_data[f"{app['name']}:{app['port']}"] = {
            "web_apm": get_web_apm(app)
        }
    return apm_data
