#!/bin/bash

echo "Installing pip3"
sudo apt install python3-pip
echo "Installing Python dependencies"
pip3 install -r /home/ubuntu/predictor/requirements.txt
echo "Server 5000"
http-server /home/ubuntu/predictor -p 5000