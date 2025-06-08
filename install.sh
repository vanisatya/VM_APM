#!/bin/bash

# Ensure Unix line endings
command -v dos2unix >/dev/null 2>&1 || sudo apt-get update && sudo apt-get install -y dos2unix

echo "📦 Installing VM APM components..."

# Clean up existing APM processes
pkill -f web_apm.py
pkill -f server_apm.py

# Download files
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/server_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/web_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/requirements.txt

# Convert to Unix format
dos2unix server_apm.py web_apm.py requirements.txt

# Install Python dependencies
pip3 install --user -r requirements.txt

# Set API endpoint
export API_ENDPOINT="https://vm-apm.onrender.com/metrics/upload"

echo "🚀 Starting APM agents with endpoint: $API_ENDPOINT"

# Start agents in background
nohup python3 server_apm.py > server_apm.log 2>&1 &
nohup python3 web_apm.py > web_apm.log 2>&1 &

echo "✅ VM APM agents installed and running."
