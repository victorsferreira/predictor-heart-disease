#!/bin/bash

echo "Installing pip3"
sudo apt install python3-pip
echo "Installing Python dependencies"
pip3 install -r /home/ubuntu/predictor/requirements.txt
echo "Server 5000"
# nohup http-server /home/ubuntu/predictor -p 5000 </dev/null &>/dev/null &
nohup python3 /home/ubuntu/predictor/src/server/server.py </dev/null &>/dev/null &