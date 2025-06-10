#!/bin/bash

echo "🔧 Starting VM APM Installation..."

# Run Server APM in background and log output
nohup python3 server_apm.py > server_apm.log 2>&1 &

# Run Web APM in background and log output
nohup python3 web_apm.py > web_apm.log 2>&1 &

echo "✅ VM APM agents (server & web) launched successfully."
