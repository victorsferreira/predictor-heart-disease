#!/bin/bash

ls
sudo apt install python3-pip
pip3 install -r /home/ubuntu/predictor/requirements.txt
python3 /home/ubuntu/predictor/server.py