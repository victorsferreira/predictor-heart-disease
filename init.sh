#!/bin/bash

sudo apt install python3-pip
pip3 install -r ${PWD}/requirements.txt
python3 ${PWD}/server.py