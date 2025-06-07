#!/bin/bash

echo "📦 Installing VM APM components..."

# Download agent scripts
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/server_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/web_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/requirements.txt

# Install dependencies
pip3 install -r requirements.txt --user

# Set your Render API endpoint
RENDER_ENDPOINT="https://vm-apm.onrender.com/metrics/upload"

# Start APM agents with the API endpoint passed via env variable
echo "🚀 Starting APM agents with endpoint: $RENDER_ENDPOINT"

nohup env API_ENDPOINT=$RENDER_ENDPOINT python3 server_apm.py > server_apm.log 2>&1 &
nohup env API_ENDPOINT=$RENDER_ENDPOINT python3 web_apm.py > web_apm.log 2>&1 &

echo "✅ VM APM agents installed and running."
