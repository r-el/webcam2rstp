#!/usr/bin/env python3
"""
Complete RTSP Webcam Streaming Solution
Starts MediaMTX server and streams webcam to it
"""

import cv2
import subprocess
import argparse
import socket
import time
import sys
import os
import threading
import signal

class RTSPStreamer:
    def __init__(self):
        self.mediamtx_process = None
        self.ffmpeg_process = None
        self.running = False
        
    def get_local_ip(self):
        """Get local IP address"""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 1))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = '127.0.0.1'
        finally:
            s.close()
        return local_ip
    
    def start_mediamtx(self):
        """Start MediaMTX RTSP server"""
        mediamtx_path = './mediamtx'
        if not os.path.exists(mediamtx_path):
            print("Error: MediaMTX binary not found!")
            print("Please download MediaMTX from https://github.com/bluenviron/mediamtx/releases")
            return False
            
        print("Starting MediaMTX RTSP server...")
        self.mediamtx_process = subprocess.Popen(
            [mediamtx_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait a moment for MediaMTX to start
        time.sleep(2)
        
        if self.mediamtx_process.poll() is None:
            print("MediaMTX started successfully")
            return True
        else:
            print("Failed to start MediaMTX")
            return False
    
    def start_ffmpeg_stream(self, camera_device, width, height, fps, port):
        """Start FFmpeg streaming to MediaMTX"""
        if not os.path.exists(camera_device):
            print(f"Error: Camera device {camera_device} not found")
            return False
            
        command = [
            'ffmpeg',
            '-f', 'v4l2',
            '-video_size', f'{width}x{height}',
            '-framerate', str(fps),
            '-i', camera_device,
            '-c:v', 'libx264',
            '-preset', 'ultrafast',
            '-tune', 'zerolatency',
            '-pix_fmt', 'yuv420p',
            '-g', '30',
            '-f', 'rtsp',
            f'rtsp://localhost:{port}/stream'
        ]
        
        print(f"Starting FFmpeg stream: {' '.join(command)}")
        self.ffmpeg_process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        return True
    
    def stop_all(self):
        """Stop all processes"""
        print("\nStopping streaming...")
        self.running = False
        
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
            print("FFmpeg stopped")
        
        if self.mediamtx_process:
            self.mediamtx_process.terminate()
            self.mediamtx_process.wait()
            print("MediaMTX stopped")
    
    def monitor_processes(self):
        """Monitor running processes"""
        while self.running:
            if self.mediamtx_process and self.mediamtx_process.poll() is not None:
                print("MediaMTX process terminated unexpectedly")
                break
                
            if self.ffmpeg_process and self.ffmpeg_process.poll() is not None:
                stdout, stderr = self.ffmpeg_process.communicate()
                if stderr:
                    print("FFmpeg error:")
                    print(stderr.decode())
                break
                
            time.sleep(1)
    
    def run(self, args):
        """Main run method"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, lambda s, f: self.stop_all())
        signal.signal(signal.SIGTERM, lambda s, f: self.stop_all())
        
        try:
            # Start MediaMTX
            if not self.start_mediamtx():
                return
            
            # Start FFmpeg streaming
            if not self.start_ffmpeg_stream(args.camera, args.width, args.height, args.fps, args.port):
                return
            
            local_ip = self.get_local_ip()
            
            print("\n" + "="*60)
            print(f"RTSP stream available on: rtsp://{local_ip}:{args.port}/stream")
            print("You can view the stream with:")
            print("  VLC: Open Network Stream -> rtsp://YOUR_IP:8554/stream")
            print("  FFplay: ffplay rtsp://YOUR_IP:8554/stream")
            print("="*60 + "\n")
            
            self.running = True
            
            # Monitor processes
            print("Press Ctrl+C to stop streaming")
            self.monitor_processes()
            
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()

def main():
    parser = argparse.ArgumentParser(description='Complete RTSP Webcam Streaming')
    parser.add_argument('--camera', type=str, default='/dev/video0', help='Camera device path')
    parser.add_argument('--width', type=int, default=640, help='Stream width')
    parser.add_argument('--height', type=int, default=480, help='Stream height')
    parser.add_argument('--fps', type=int, default=15, help='Stream FPS')
    parser.add_argument('--port', type=int, default=8554, help='RTSP port')
    args = parser.parse_args()
    
    streamer = RTSPStreamer()
    streamer.run(args)

if __name__ == "__main__":
    main()
