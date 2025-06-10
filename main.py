from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import subprocess

app = FastAPI()

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# (Optional) Mount static files like CSS, JS
app.mount("/static", StaticFiles(directory="static"), name="static")

# GET endpoint for dashboard page
@app.get("/", response_class=HTMLResponse)
def get_dashboard(request: Request):
    return templates.TemplateResponse("Dashboard.html", {"request": request})

# POST endpoint to trigger install.sh
@app.post("/install")
def install_vm_apm():
    try:
        subprocess.Popen(["bash", "install.sh"])
        return {"status": "VM APM installation started"}
    except Exception as e:
        return {"error": str(e)}
