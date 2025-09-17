#!/bin/bash

# Webcam Streaming Service Setup Script
# Works on Ubuntu/Debian Linux

echo "Setting up Webcam Streaming Service..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Installing..."
    sudo apt-get update
    sudo apt-get install -y python3 python3-pip python3-venv
fi

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install opencv-python numpy

# Make the script executable
chmod +x webcam_http_stream.py

echo "Setup complete!"
echo ""
echo "To start streaming:"
echo "1. Activate environment: source .venv/bin/activate"
echo "2. Run: python webcam_http_stream.py"
echo ""
echo "Or run directly: .venv/bin/python webcam_http_stream.py"
