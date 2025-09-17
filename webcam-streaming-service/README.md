# Webcam Streaming Service

This project provides a simple solution for streaming webcam video over the internet using WebRTC. It allows users to share their webcam feed with others in real-time.

## Features

- Access webcam video streams from any device (Windows or Linux).
- Real-time video streaming using WebRTC.
- Simple API for starting and stopping streams.
- Docker support for easy deployment.

## Project Structure

```
webcam-streaming-service
├── src
│   ├── server.js          # Entry point of the application
│   ├── stream
│   │   ├── camera.js      # Handles webcam access
│   │   └── webrtc.js      # Manages WebRTC connections
│   ├── api
│   │   └── routes.js      # Defines API routes
│   └── config
│       └── default.js     # Configuration settings
├── public
│   ├── index.html         # Main HTML page
│   ├── js
│   │   └── client.js      # Client-side JavaScript
│   └── css
│       └── style.css      # Styles for the application
├── Dockerfile              # Docker image setup
├── docker-compose.yml      # Docker services configuration
├── package.json            # npm configuration
└── README.md               # Project documentation
```

## Getting Started

### Prerequisites

- Node.js and npm installed on your machine.
- Docker and Docker Compose (if you want to run the application in a container).

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd webcam-streaming-service
   ```

2. Install dependencies:
   ```
   npm install
   ```

### Running the Application

You can run the application in two ways: directly using Node.js or using Docker.

#### Using Node.js

1. Start the server:
   ```
   node src/server.js
   ```

2. Open your browser and navigate to `http://localhost:3000` to access the application.

#### Using Docker

1. Build the Docker image:
   ```
   docker-compose build
   ```

2. Run the application:
   ```
   docker-compose up
   ```

3. Open your browser and navigate to `http://localhost:3000` to access the application.

## Usage

- Once the application is running, you can start streaming your webcam by clicking the "Start Stream" button on the web interface.
- To stop the stream, click the "Stop Stream" button.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.