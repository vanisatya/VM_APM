from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from subprocess import Popen
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

metrics_dict = {}

@app.get("/")
def serve_dashboard():
    return FileResponse("static/Dashboard.html")

@app.post("/install")
def install_vm_apm():
    """Simulate VM install trigger. In real world, this might SSH or notify a deployment tool."""
    # For local testing only:
    try:
        Popen(["bash", "install.sh"])
        return {"status": "install triggered"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}

@app.post("/metrics/upload")
async def upload_metrics(payload: dict):
    for app_name, metrics in payload.items():
        if app_name not in metrics_dict:
            metrics_dict[app_name] = {}
        metrics_dict[app_name].update(metrics)
    return {"status": "success"}

@app.get("/metrics")
def get_metrics():
    return JSONResponse(content=metrics_dict)
