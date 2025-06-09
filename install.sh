#!/bin/bash

echo "🔧 Installing VM APM agents..."

# Ensure script is run from the correct directory
cd "$(dirname "$0")"

# Make scripts executable
chmod +x server_apm.py web_apm.py

# Install required packages
echo "📦 Installing dependencies..."
sudo apt-get update -y
sudo apt-get install -y python3-pip curl lsof net-tools

# Install Python packages
pip3 install --upgrade pip
pip3 install psutil requests

# Kill any previous instances
echo "🧹 Cleaning up old APM agents..."
pkill -f server_apm.py
pkill -f web_apm.py

# Start Web APM (user permissions are fine)
echo "🚀 Starting Web APM..."
nohup python3 web_apm.py > web_apm.log 2>&1 &

# Start Server APM (needs sudo)
echo "🚀 Starting Server APM with sudo..."
nohup sudo python3 server_apm.py > server_apm.log 2>&1 &

echo "✅ VM APM agents installed and running in background."
