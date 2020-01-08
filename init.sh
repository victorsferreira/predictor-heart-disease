#!/bin/bash

echo `Installing pip3`
sudo apt install python3-pip
echo `Installing Python dependencies`
pip3 install -r /home/ubuntu/predictor/requirements.txt
echo `Will start server on port 5000`
python3 /home/ubuntu/predictor/server.py &