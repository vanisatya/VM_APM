from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
metrics_dict = {}

# Allow CORS (optional but helpful if your dashboard is web-based)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "VM APM Dashboard API is running"}

@app.post("/metrics/upload")
async def upload_metrics(request: Request):
    try:
        data = await request.json()
        hostname = data.get("hostname", "unknown_host")
        metrics = data.get("metrics", {})

        for app_name, app_metrics in metrics.items():
            key = f"{hostname}:{app_name}"
            if key not in metrics_dict:
                metrics_dict[key] = {}
            metrics_dict[key].update(app_metrics)

        return JSONResponse(content={"status": "success"}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/metrics")
def get_all_metrics():
    return metrics_dict
