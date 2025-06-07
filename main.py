from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# Serve static dashboard
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_dashboard():
    return FileResponse("static/Dashboard.html")

# Allow CORS (so VM or frontend can talk to this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store: { vm_id: { app_key: { web_apm, server_apm } } }
global_metrics = {}

@app.post("/metrics/upload")
async def upload_metrics(request: Request):
    data = await request.json()
    vm_id = data.get("vm_id")
    metrics = data.get("metrics")
    if vm_id and metrics:
        global_metrics[vm_id] = metrics
        return {"status": "success", "message": f"Metrics received from {vm_id}"}
    return {"status": "error", "message": "Invalid data format"}

@app.get("/metrics")
def get_all_metrics():
    return JSONResponse(content=global_metrics)
