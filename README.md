# Webcam HTTP Streaming Service

Simple webcam streaming service that broadcasts your camera feed over HTTP. Works on Windows and Linux.

## Features

- HTTP streaming (works in any web browser)
- Lightweight and efficient
- Easy to deploy with Docker
- Configurable resolution and frame rate
- Cross-platform support

## Quick Start

### Option 1: Run with Python

1. Install dependencies:
```bash
pip install opencv-python numpy
```

2. Run the streaming service:
```bash
python webcam_http_stream.py
```

3. Open your browser and go to: `http://YOUR_IP:8080`

### Option 2: Run with Docker

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. Open your browser and go to: `http://YOUR_IP:8080`

## Configuration

You can customize the stream with command line arguments:

```bash
python webcam_http_stream.py --width 1280 --height 720 --fps 30 --port 8080 --camera 0
```

Parameters:
- `--camera`: Camera device index (default: 0)
- `--width`: Stream width in pixels (default: 640)
- `--height`: Stream height in pixels (default: 480)
- `--fps`: Frames per second (default: 15)
- `--port`: HTTP port (default: 8080)

## Accessing from Internet

To allow access from outside your local network:

1. **Port Forwarding**: Configure your router to forward port 8080 to your computer
2. **Use External IP**: Share your public IP address with the port (e.g., `http://YOUR_PUBLIC_IP:8080`)

## Browser Compatibility

The stream works in all modern browsers including:
- Chrome
- Firefox
- Safari
- Edge

## System Requirements

- Python 3.8+
- Webcam or camera device
- 1GB RAM (recommended)
- Network connection

## Troubleshooting

### Camera not detected
- Check if camera is connected: `ls /dev/video*` (Linux)
- Try different camera index: `--camera 1`

### Permission denied
- Run with sudo (Linux): `sudo python webcam_http_stream.py`
- Check camera permissions

### Low performance
- Reduce resolution: `--width 320 --height 240`
- Reduce frame rate: `--fps 10`

## Security Note

This service broadcasts your camera feed over HTTP without authentication. Only run on trusted networks or implement additional security measures for public use.
