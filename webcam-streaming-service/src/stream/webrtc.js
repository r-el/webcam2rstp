const express = require('express');
const { Server } = require('socket.io');
const http = require('http');

const app = express();
const server = http.createServer(app);
const io = new Server(server);

let clients = [];

io.on('connection', (socket) => {
    console.log('A user connected: ' + socket.id);
    clients.push(socket);

    socket.on('disconnect', () => {
        console.log('User disconnected: ' + socket.id);
        clients = clients.filter(client => client !== socket);
    });

    socket.on('offer', (offer) => {
        socket.broadcast.emit('offer', offer);
    });

    socket.on('answer', (answer) => {
        socket.broadcast.emit('answer', answer);
    });

    socket.on('candidate', (candidate) => {
        socket.broadcast.emit('candidate', candidate);
    });
});

const startWebRTCServer = (port) => {
    server.listen(port, () => {
        console.log(`WebRTC server is running on port ${port}`);
    });
};

module.exports = { startWebRTCServer };