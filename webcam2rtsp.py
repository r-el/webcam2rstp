import cv2
import subprocess
import argparse
import socket
import numpy as np
import time
import sys
import os

def get_local_ip():
    """Get local IP address to display streaming URL"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('8.8.8.8', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

def start_rtsp_server(width, height, fps, port):
    """Start FFmpeg RTSP publisher to MediaMTX server"""
    command = [
        'ffmpeg',
        '-f', 'v4l2',
        '-video_size', f'{width}x{height}',
        '-framerate', str(fps),
        '-i', '/dev/video0',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-tune', 'zerolatency',
        '-pix_fmt', 'yuv420p',
        '-g', '30',  # GOP size
        '-f', 'rtsp',
        f'rtsp://localhost:{port}/stream'
    ]
    
    print(f"Starting FFmpeg with command: {' '.join(command)}")
    
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    return process

def main():
    parser = argparse.ArgumentParser(description='Stream webcam to RTSP')
    parser.add_argument('--camera', type=str, default='/dev/video0', help='Camera device path')
    parser.add_argument('--width', type=int, default=640, help='Stream width')
    parser.add_argument('--height', type=int, default=480, help='Stream height')
    parser.add_argument('--fps', type=int, default=30, help='Stream FPS')
    parser.add_argument('--port', type=int, default=8554, help='RTSP port')
    args = parser.parse_args()
    
    # Check if camera device exists
    if not os.path.exists(args.camera):
        print(f"Error: Camera device {args.camera} not found")
        return
    
    # Start RTSP server
    process = start_rtsp_server(args.width, args.height, args.fps, args.port)
    
    # Get local IP for connection URL
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print(f"RTSP stream available on: rtsp://{local_ip}:{args.port}/stream")
    print("You can view the stream with VLC or similar RTSP-capable players")
    print("MediaMTX server must be running on localhost")
    print("="*60 + "\n")
    
    print("Press Ctrl+C to stop streaming")
    
    try:
        # Wait and monitor the process
        while True:
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                print("FFmpeg output:")
                if stdout:
                    print(stdout.decode())
                if stderr:
                    print("Errors:")
                    print(stderr.decode())
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("Streaming stopped by user")
    finally:
        # Clean up
        if process:
            process.terminate()
            process.wait()
        print("Stream ended and resources released")

if __name__ == "__main__":
    main()
