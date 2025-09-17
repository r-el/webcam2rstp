# Use Python slim image for smaller size
FROM python:3.12-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libopencv-dev \
    python3-opencv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the HTTP port
EXPOSE 8080

# Run the streaming application
CMD ["python", "webcam_http_stream.py", "--width", "640", "--height", "480", "--fps", "15", "--port", "8080"]
