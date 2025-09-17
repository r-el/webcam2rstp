# Webcam RTSP Streaming Service

Simple webcam streaming service that broadcasts your camera feed over RTSP protocol. Works on Windows and Linux.

## Features

- Real RTSP streaming (compatible with all RTSP clients)
- Uses MediaMTX for professional RTSP server
- Lightweight and efficient
- Easy to deploy with single script
- Configurable resolution and frame rate
- Cross-platform support

## Quick Start

### Linux (Recommended)

1. Run the setup script:
```bash
chmod +x start_rtsp_stream.sh
./start_rtsp_stream.sh
```

2. Open the stream in VLC or any RTSP client:
   - Open VLC -> Media -> Open Network Stream
   - Enter: `rtsp://YOUR_IP:8554/stream`

### Manual Setup

1. Install dependencies:
```bash
pip install opencv-python numpy
```

2. Download MediaMTX (RTSP server):
```bash
wget https://github.com/bluenviron/mediamtx/releases/download/v1.8.0/mediamtx_v1.8.0_linux_amd64.tar.gz
tar -xzf mediamtx_v1.8.0_linux_amd64.tar.gz
```

3. Run the complete streaming service:
```bash
python complete_rtsp_streamer.py
```

## Configuration

You can customize the stream with command line arguments:

```bash
./start_rtsp_stream.sh --width 1280 --height 720 --fps 30 --camera /dev/video0
```

Parameters:

- `--camera`: Camera device path (default: /dev/video0)
- `--width`: Stream width in pixels (default: 640)
- `--height`: Stream height in pixels (default: 480)
- `--fps`: Frames per second (default: 15)
- `--port`: RTSP port (default: 8554)

## RTSP Client Compatibility

The stream works with all standard RTSP clients:

- **VLC Media Player**: Most popular option
- **FFplay**: Command line: `ffplay rtsp://IP:8554/stream`
- **OBS Studio**: Add Media Source with RTSP URL
- **Mobile apps**: VLC for Android/iOS
- **Security cameras software**
- **Web browsers** (with WebRTC conversion)

## Accessing from Internet

To allow access from outside your local network:

1. **Port Forwarding**: Configure your router to forward port 8554 to your computer
2. **Use External IP**: Share your public IP address with the port (e.g., `rtsp://YOUR_PUBLIC_IP:8554/stream`)

## System Requirements

- Python 3.8+
- FFmpeg installed on system
- Webcam or camera device
- 1GB RAM (recommended)
- Network connection

## Troubleshooting

### Camera not detected

- Check if camera is connected: `ls /dev/video*` (Linux)
- Try different camera device: `--camera /dev/video1`

### Permission denied

- Run with sudo (Linux): `sudo ./start_rtsp_stream.sh`
- Check camera permissions

### Low performance

- Reduce resolution: `--width 320 --height 240`
- Reduce frame rate: `--fps 10`

### RTSP connection issues

- Check firewall settings
- Ensure port 8554 is not blocked
- Try different RTSP client

## Files Description

- `start_rtsp_stream.sh`: Simple launcher script (Linux)
- `complete_rtsp_streamer.py`: Complete Python solution
- `webcam2rtsp.py`: Basic RTSP streaming script
- `webcam_http_stream.py`: HTTP streaming alternative
- `mediamtx`: RTSP server binary

## Security Note

This service broadcasts your camera feed over RTSP without authentication. Only run on trusted networks or implement additional security measures for public use.
