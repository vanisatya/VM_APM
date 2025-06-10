from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory store for latest metrics
latest_metrics = {}

@app.get("/", response_class=HTMLResponse)
def get_dashboard(request: Request):
    return templates.TemplateResponse("Dashboard.html", {"request": request})

@app.post("/install")
def install_vm_apm():
    try:
        subprocess.Popen(["bash", "install.sh"])
        return {"status": "VM APM installation started"}
    except Exception as e:
        return {"error": str(e)}

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
