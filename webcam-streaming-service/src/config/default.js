module.exports = {
    serverPort: process.env.SERVER_PORT || 3000,
    webrtcConfig: {
        iceServers: [
            {
                urls: 'stun:stun.l.google.com:19302'
            }
        ]
    },
    streamSettings: {
        video: {
            width: 1280,
            height: 720,
            frameRate: 30
        },
        audio: true
    }
};