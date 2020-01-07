#!/bin/bash

# sudo chown ubuntu -R ./
# sudo chmod +x -R ./
sudo apt install python3-pip
pip3 install -r requirements.txt
python3 server.py