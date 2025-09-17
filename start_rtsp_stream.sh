#!/bin/bash

# Simple RTSP Webcam Streaming Launcher
echo "Starting RTSP Webcam Streaming Service..."

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "Setting up Python environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install opencv-python numpy
else
    source .venv/bin/activate
fi

# Check if MediaMTX exists
if [ ! -f "./mediamtx" ]; then
    echo "MediaMTX not found. Downloading..."
    wget -q https://github.com/bluenviron/mediamtx/releases/download/v1.8.0/mediamtx_v1.8.0_linux_amd64.tar.gz
    tar -xzf mediamtx_v1.8.0_linux_amd64.tar.gz
    rm mediamtx_v1.8.0_linux_amd64.tar.gz
fi

# Get local IP
LOCAL_IP=$(ip route get 8.8.8.8 | awk '{print $7; exit}')

echo "Starting RTSP stream..."
echo "Stream will be available at: rtsp://$LOCAL_IP:8554/stream"
echo "Press Ctrl+C to stop"

# Run the streaming service
python complete_rtsp_streamer.py "$@"
