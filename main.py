from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import json
import os

app = FastAPI()

# Serve dashboard.html and install scripts
app.mount("/static", StaticFiles(directory="static"), name="static")

STORAGE_FILE = "metrics_store.json"

def read_metrics():
    if not os.path.exists(STORAGE_FILE):
        return {}
    try:
        with open(STORAGE_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def write_metrics(data):
    with open(STORAGE_FILE, "w") as f:
        json.dump(data, f)

@app.get("/", response_class=HTMLResponse)
def root():
    try:
        with open("static/dashboard.html", "r") as f:
            return f.read()
    except:
        return HTMLResponse("<h1>VM APM Dashboard is running, but dashboard.html not found</h1>")

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
