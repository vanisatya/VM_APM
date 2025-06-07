#!/bin/bash

echo "📦 Installing VM APM components..."

# Download the latest versions
echo "📥 Downloading APM files..."
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/server_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/web_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/requirements.txt

# Install dependencies
echo "📦 Installing Python packages..."
pip3 install -r requirements.txt --user

# Export API endpoint
export API_ENDPOINT="https://your-render-app.onrender.com/metrics/upload"  # 🔁 Replace this

# Run both scripts in background
echo "🚀 Starting APM agents..."
nohup python3 server_apm.py > server_apm.log 2>&1 &
nohup python3 web_apm.py > web_apm.log 2>&1 &

echo "✅ VM APM agents are running."
