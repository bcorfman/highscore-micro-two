#!/bin/bash
sudo apt update
sudo apt install -y make curl
sudo apt clean
pip install --upgrade pip
pip install -r requirements-dev.lock