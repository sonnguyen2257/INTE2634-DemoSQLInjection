#!/bin/bash

# Create a new virtual environment in the current directory
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install all dependencies listed in requirements.txt from the local directory
pip install -r requirements.txt

python3 app.py
