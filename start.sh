#!/bin/bash

echo "======================================"
echo "  SkillLens AI - Career Intelligence"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "[ERROR] Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

echo "[INFO] Python found: $(python3 --version)"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "[INFO] Creating virtual environment..."
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo "[ERROR] Failed to create virtual environment"
        exit 1
    fi
    echo "[SUCCESS] Virtual environment created"
    echo ""
fi

# Activate virtual environment
echo "[INFO] Activating virtual environment..."
source venv/bin/activate
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to activate virtual environment"
    exit 1
fi

# Install dependencies
echo "[INFO] Installing dependencies..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "[ERROR] Failed to install dependencies"
    exit 1
fi
echo "[SUCCESS] Dependencies installed"
echo ""

# Create necessary directories
mkdir -p database uploads models

echo "[INFO] Starting SkillLens AI server..."
echo ""
echo "======================================"
echo "  Server running at:"
echo "  http://127.0.0.1:5000"
echo "======================================"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the Flask server
cd backend
python3 app.py

# Deactivate virtual environment on exit
cd ..
deactivate
