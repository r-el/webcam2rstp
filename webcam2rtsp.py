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
    """Start FFmpeg RTSP server process"""
    command = [
        'ffmpeg',
        '-y',  # Overwrite output files
        '-f', 'rawvideo',
        '-pixel_format', 'bgr24',
        '-video_size', f'{width}x{height}',
        '-framerate', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-tune', 'zerolatency',
        '-pix_fmt', 'yuv420p',
        '-g', '50',  # GOP size
        '-f', 'rtsp',
        '-rtsp_transport', 'tcp',
        f'rtsp://0.0.0.0:{port}/live'
    ]
    
    process = subprocess.Popen(
        command, 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    return process

def main():
    parser = argparse.ArgumentParser(description='Stream webcam to RTSP')
    parser.add_argument('--camera', type=int, default=0, help='Camera device index')
    parser.add_argument('--width', type=int, default=640, help='Stream width')
    parser.add_argument('--height', type=int, default=480, help='Stream height')
    parser.add_argument('--fps', type=int, default=30, help='Stream FPS')
    parser.add_argument('--port', type=int, default=8554, help='RTSP port')
    args = parser.parse_args()
    
    # Open webcam
    cap = cv2.VideoCapture(args.camera)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    cap.set(cv2.CAP_PROP_FPS, args.fps)
    
    # Get actual camera properties (might be different from requested)
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    actual_fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"Camera initialized: {actual_width}x{actual_height} @ {actual_fps}fps")
    
    # Start RTSP server
    process = start_rtsp_server(actual_width, actual_height, actual_fps, args.port)
    
    # Get local IP for connection URL
    local_ip = get_local_ip()
    
    print("\n" + "="*60)
    print(f"RTSP stream started on: rtsp://{local_ip}:{args.port}/live")
    print("You can view the stream with VLC or similar RTSP-capable players")
    print("="*60 + "\n")
    
    print("Press Ctrl+C to stop streaming")
    
    try:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading from webcam")
                break
            
            frame_count += 1
            if frame_count % 30 == 0:  # Print status every 30 frames
                print(f"Streaming frame {frame_count}...")
            
            # Check if FFmpeg process is still running
            if process.poll() is not None:
                print("FFmpeg process terminated")
                break
            
            try:
                # Write frame to FFmpeg stdin
                process.stdin.write(frame.tobytes())
                process.stdin.flush()
            except BrokenPipeError:
                print("FFmpeg pipe broken, stopping stream")
                break
            
            # Small delay to control frame rate
            time.sleep(1.0 / actual_fps)
            
    except KeyboardInterrupt:
        print("Streaming stopped by user")
    finally:
        # Clean up
        if process:
            try:
                process.stdin.close()
            except:
                pass
            process.terminate()
            process.wait()
        cap.release()
        print("Stream ended and resources released")

if __name__ == "__main__":
    main()
