import cv2
import threading
import argparse
import socket
import time
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class VideoStreamHandler(BaseHTTPRequestHandler):
    """HTTP request handler for video streaming"""
    
    def do_GET(self):
        if self.path == '/':
            self.send_html_page()
        elif self.path == '/stream':
            self.send_video_stream()
        else:
            self.send_error(404, "Page not found")
    
    def send_html_page(self):
        """Send HTML page with video player"""
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Webcam Stream</title>
            <style>
                body { 
                    font-family: Arial, sans-serif; 
                    text-align: center; 
                    background-color: #f0f0f0;
                }
                .container { 
                    max-width: 800px; 
                    margin: 0 auto; 
                    padding: 20px;
                }
                img { 
                    max-width: 100%; 
                    border: 2px solid #333;
                    border-radius: 10px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Live Webcam Stream</h1>
                <img src="/stream" alt="Live Stream">
                <p>Streaming from your webcam</p>
            </div>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def send_video_stream(self):
        """Send MJPEG video stream"""
        self.send_response(200)
        self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=frame')
        self.end_headers()
        
        try:
            while True:
                if hasattr(self.server, 'latest_frame') and self.server.latest_frame is not None:
                    # Encode frame as JPEG
                    ret, jpeg = cv2.imencode('.jpg', self.server.latest_frame, 
                                           [cv2.IMWRITE_JPEG_QUALITY, 80])
                    if ret:
                        frame_data = jpeg.tobytes()
                        
                        # Send frame in MJPEG format
                        self.wfile.write(b'--frame\r\n')
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', str(len(frame_data)))
                        self.end_headers()
                        self.wfile.write(frame_data)
                        self.wfile.write(b'\r\n')
                
                time.sleep(0.1)  # Control frame rate
                
        except Exception as e:
            print(f"Stream error: {e}")

def get_local_ip():
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

def camera_thread(camera_index, width, height, fps, server):
    """Camera capture thread"""
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not open webcam")
        return
    
    # Set camera properties
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap.set(cv2.CAP_PROP_FPS, fps)
    
    actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    actual_fps = int(cap.get(cv2.CAP_PROP_FPS))
    
    print(f"Camera initialized: {actual_width}x{actual_height} @ {actual_fps}fps")
    
    frame_delay = 1.0 / fps
    
    try:
        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error reading from webcam")
                break
            
            # Store latest frame in server
            server.latest_frame = frame
            
            frame_count += 1
            if frame_count % 100 == 0:
                print(f"Captured {frame_count} frames")
            
            time.sleep(frame_delay)
            
    except Exception as e:
        print(f"Camera error: {e}")
    finally:
        cap.release()
        print("Camera released")

def main():
    parser = argparse.ArgumentParser(description='Stream webcam via HTTP')
    parser.add_argument('--camera', type=int, default=0, help='Camera device index')
    parser.add_argument('--width', type=int, default=640, help='Stream width')
    parser.add_argument('--height', type=int, default=480, help='Stream height')
    parser.add_argument('--fps', type=int, default=15, help='Stream FPS')
    parser.add_argument('--port', type=int, default=8080, help='HTTP port')
    args = parser.parse_args()
    
    # Get local IP
    local_ip = get_local_ip()
    
    # Create HTTP server
    server = HTTPServer(('0.0.0.0', args.port), VideoStreamHandler)
    server.latest_frame = None
    
    print("\n" + "="*60)
    print(f"HTTP stream started on: http://{local_ip}:{args.port}")
    print("Open this URL in any web browser to view the stream")
    print("="*60 + "\n")
    
    # Start camera thread
    cam_thread = threading.Thread(
        target=camera_thread, 
        args=(args.camera, args.width, args.height, args.fps, server)
    )
    cam_thread.daemon = True
    cam_thread.start()
    
    print("Press Ctrl+C to stop streaming")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStreaming stopped by user")
    finally:
        server.shutdown()
        print("Server stopped")

if __name__ == "__main__":
    main()
