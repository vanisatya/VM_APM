from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

metrics_dict = {}

@app.get("/")
def serve_dashboard():
    return FileResponse("static/Dashboard.html")

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
