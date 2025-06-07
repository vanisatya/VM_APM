#!/bin/bash

echo "📦 Installing APM Agent..."

# Create working directory
mkdir -p ~/apm_agent/static
cd ~/apm_agent || exit 1

# Download Python files from GitHub
echo "📥 Downloading files..."
curl -O https://raw.githubusercontent.com/VaniSatya/VM_APM/master/main.py
curl -O https://raw.githubusercontent.com/VaniSatya/VM_APM/master/web_apm.py
curl -O https://raw.githubusercontent.com/VaniSatya/VM_APM/master/server_apm.py
curl -O https://raw.githubusercontent.com/VaniSatya/VM_APM/master/requirements.txt
curl -o static/Dashboard.html https://raw.githubusercontent.com/VaniSatya/VM_APM/master/static/Dashboard.html

# Install required Python packages
echo "📦 Installing Python packages..."
pip3 install --user -r requirements.txt

# Start the FastAPI app
echo "🚀 Starting APM Agent..."
nohup python3 -m uvicorn main:app --host 0.0.0.0 --port 8010 > apm.log 2>&1 &

echo "✅ APM Agent installed and running at http://<VM-IP>:8010/"
