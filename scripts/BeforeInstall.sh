#!/bin/bash

echo "Stop Python process"
sudo killall python3 || true
echo "Stop Server process"
sudo kill $(lsof -t -i:5000) || true