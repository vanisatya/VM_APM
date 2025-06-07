import psutil

def get_server_apm(pid):
    try:
        proc = psutil.Process(pid)
        cpu = proc.cpu_percent(interval=1)
        mem = proc.memory_info().rss / (1024 ** 2)  # MB
        return {
            "CPU (%)": cpu,
            "Memory (MB)": round(mem, 2)
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return {
            "CPU (%)": -1,
            "Memory (MB)": -1
        }

def collect_all_server_apm():
    apm = {}
    for conn in psutil.net_connections(kind="inet"):
        if conn.status == psutil.CONN_LISTEN:
            pid = conn.pid
            port = conn.laddr.port
            if pid and port:
                proc_name = psutil.Process(pid).name()
                key = f"{proc_name}:{port}"
                apm[key] = {
                    "server_apm": get_server_apm(pid)
                }
    return apm
