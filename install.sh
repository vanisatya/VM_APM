#!/bin/bash

echo "📦 Installing VM APM components..."

# Download latest scripts
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/server_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/web_apm.py
curl -s -O https://raw.githubusercontent.com/vanisatya/VM_APM/master/requirements.txt

# Convert to UNIX format in case line endings are wrong
sed -i 's/\r$//' server_apm.py
sed -i 's/\r$//' web_apm.py
sed -i 's/\r$//' requirements.txt

# Install Python dependencies
pip3 install --user -r requirements.txt

# Set API endpoint as environment variable
export API_ENDPOINT="https://vm-apm.onrender.com/metrics/upload"
echo "🚀 Starting APM agents with endpoint: $API_ENDPOINT"

# Start agents in background and log output
nohup python3 server_apm.py > server_apm.log 2>&1 &
nohup python3 web_apm.py > web_apm.log 2>&1 &

echo "✅ VM APM agents installed and running."
