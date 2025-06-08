from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()
metrics_dict = {}

@app.get("/")
def root():
    return {"message": "VM APM dashboard is running"}

@app.post("/metrics/upload")
async def upload_metrics(request: Request):
    try:
        data = await request.json()

        hostname = data.get("hostname", "unknown_host")
        metrics = data.get("metrics", {})

        if not metrics:
            return JSONResponse(content={"status": "no metrics received"}, status_code=200)

        # ✅ Store metrics under hostname -> app_name -> metric_type
        for app_name, app_data in metrics.items():
            if hostname not in metrics_dict:
                metrics_dict[hostname] = {}
            metrics_dict[hostname][app_name] = app_data

        return JSONResponse(content={"status": "success"}, status_code=200)

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/metrics")
def get_metrics():
    return metrics_dict
