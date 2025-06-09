from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Dict, Any
import os

app = FastAPI()

# Serve HTML from templates/
templates = Jinja2Templates(directory="templates")

# Serve static assets (optional if you have CSS/JS/images)
app.mount("/static", StaticFiles(directory="static"), name="static")

# In-memory storage for APM metrics
metrics_store: Dict[str, Dict[str, Any]] = {}

class APMUpload(BaseModel):
    hostname: str
    metrics: Dict[str, Dict[str, Dict[str, Any]]]

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse("Dashboard.html", {"request": request})

@app.post("/metrics/upload")
async def upload_metrics(data: APMUpload):
    for app_name, metric_types in data.metrics.items():
        full_app_name = f"{data.hostname}::{app_name}"
        if full_app_name not in metrics_store:
            metrics_store[full_app_name] = {}
        metrics_store[full_app_name].update(metric_types)
    return {"status": "ok"}

@app.get("/metrics")
async def get_metrics():
    return JSONResponse(content=metrics_store)
