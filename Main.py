from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from web_apm import collect_all_web_apm
from server_apm import collect_all_server_apm

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def serve_dashboard():
    return FileResponse("static/Dashboard.html")

@app.get("/metrics")
def get_metrics():
    web_metrics = collect_all_web_apm()
    server_metrics = collect_all_server_apm()

    merged = {}
    for app_key in set(web_metrics.keys()).union(server_metrics.keys()):
        merged[app_key] = {}
        if app_key in web_metrics:
            merged[app_key]["web_apm"] = web_metrics[app_key]["web_apm"]
        if app_key in server_metrics:
            merged[app_key]["server_apm"] = server_metrics[app_key]["server_apm"]

    return JSONResponse(content=merged)
