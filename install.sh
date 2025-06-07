echo "📦 Installing VM APM components..."

# Download files
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/server_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/web_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/requirements.txt

# Install dependencies
pip3 install -r requirements.txt --user

# Export API endpoint
export API_ENDPOINT="https://your-render-app.onrender.com/metrics/upload"

# Run agents in background
nohup python3 server_apm.py > server_apm.log 2>&1 &
nohup python3 web_apm.py > web_apm.log 2>&1 &


# Dashboard.html (served by Render)
# (Refer to previous HTML block for updated dashboard with install instruction + Live APM button)

