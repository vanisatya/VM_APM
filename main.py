from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
import subprocess
import json
import os

app = FastAPI()
STORAGE_FILE = "metrics_store.json"

def read_metrics():
    if not os.path.exists(STORAGE_FILE):
        return {}
    with open(STORAGE_FILE, "r") as f:
        return json.load(f)

def write_metrics(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f)

@app.get("/")
def root():
    return FileResponse("Dashboard.html", media_type="text/html")

@app.post("/metrics/upload")
async def upload_metrics(request: Request):
    try:
        data = await request.json()
        hostname = data.get("hostname", "unknown_host")
        metrics = data.get("metrics", {})

        all_metrics = read_metrics()
        if hostname not in all_metrics:
            all_metrics[hostname] = {}
        for app_name, app_data in metrics.items():
            all_metrics[hostname][app_name] = app_data

        write_metrics(all_metrics)
        return JSONResponse(content={"status": "success"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/metrics")
def get_metrics():
    return read_metrics()

@app.post("/install")
async def install_apm_agents():
    try:
        result = subprocess.run(["bash", "install.sh"], capture_output=True, text=True)
        return {
            "status": "success",
            "output": result.stdout,
            "error": result.stderr
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}
