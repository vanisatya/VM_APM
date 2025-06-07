#!/bin/bash

echo "📦 Installing VM APM components..."

# Ensure dos2unix is available
command -v dos2unix >/dev/null 2>&1 || sudo apt-get install dos2unix -y

# Download files
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/server_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/web_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/requirements.txt

# Convert line endings to Unix format
dos2unix server_apm.py web_apm.py requirements.txt >/dev/null 2>&1

# Install dependencies
pip3 install -r requirements.txt

# Export API endpoint
export API_ENDPOINT="https://vm-apm.onrender.com/metrics/upload"
echo "🚀 Starting APM agents with endpoint: $API_ENDPOINT"

# Run agents in background
nohup python3 server_apm.py > server_apm.log 2>&1 &
nohup python3 web_apm.py > web_apm.log 2>&1 &

echo "✅ VM APM agents installed and running."
