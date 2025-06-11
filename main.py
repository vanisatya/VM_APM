from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/downloads", StaticFiles(directory="downloads"), name="downloads")

# In-memory store for latest metrics
latest_metrics = {}

@app.get("/", response_class=HTMLResponse)
def get_dashboard(request: Request):
    return templates.TemplateResponse("Dashboard.html", {"request": request})

@app.get("/metrics-dashboard", response_class=HTMLResponse)
def metrics_dashboard(request: Request):
    return templates.TemplateResponse("metrics_dashboard.html", {"request": request})

@app.get("/metrics-data", response_class=JSONResponse)
def get_metrics_data():
    return latest_metrics

@app.post("/metrics/upload")
async def receive_metrics(request: Request):
    data = await request.json()
    global latest_metrics
    latest_metrics = data
    print("📦 Received APM data:", data)
    return {"status": "received"}

@app.get("/metrics", response_class=JSONResponse)
def get_latest_metrics():
    return latest_metrics

# ✅ New route: serve the vm_apm_installer.sh file for wget
@app.get("/download_installer")
def download_installer():
    return FileResponse(
        path="downloads/vm_apm_installer.sh",
        media_type="application/x-sh",
        filename="vm_apm_installer.sh"
    )
