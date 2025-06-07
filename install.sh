#!/bin/bash

echo " Setting up APM agent..."

# 1. Update and install Python and pip if not present
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip

# 2. Install required Python packages
pip3 install fastapi uvicorn psutil requests

# 3. Create working directory
mkdir -p ~/apm_agent/static

# 4. Copy scripts (Assume they are in same directory as install.sh)
cp main.py web_apm.py server_apm.py ~/apm_agent/
cp Dashboard.html ~/apm_agent/static/

# 5. Navigate and launch the server
cd ~/apm_agent

# 6. Run FastAPI server using nohup
nohup uvicorn main:app --host 0.0.0.0 --port 8010 > apm.log 2>&1 &

echo " APM Agent installed and running at http://<VM-IP>:8010/"
