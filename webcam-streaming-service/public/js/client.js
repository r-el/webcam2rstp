const videoElement = document.getElementById('video');
const startButton = document.getElementById('start');
const stopButton = document.getElementById('stop');
let localStream;
let peerConnection;

const serverUrl = 'YOUR_SERVER_URL'; // Replace with your server URL
const configuration = {
    iceServers: [
        { urls: 'stun:stun.l.google.com:19302' }
    ]
};

startButton.onclick = async () => {
    localStream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoElement.srcObject = localStream;

    peerConnection = new RTCPeerConnection(configuration);
    localStream.getTracks().forEach(track => peerConnection.addTrack(track, localStream));

    peerConnection.onicecandidate = event => {
        if (event.candidate) {
            // Send the candidate to the server
            sendMessage('candidate', event.candidate);
        }
    };

    peerConnection.ontrack = event => {
        const remoteVideo = document.getElementById('remoteVideo');
        remoteVideo.srcObject = event.streams[0];
    };

    const offer = await peerConnection.createOffer();
    await peerConnection.setLocalDescription(offer);
    sendMessage('offer', offer);
};

stopButton.onclick = () => {
    localStream.getTracks().forEach(track => track.stop());
    peerConnection.close();
};

function sendMessage(type, payload) {
    fetch(`${serverUrl}/api/message`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ type, payload })
    });
}

async function handleMessage(message) {
    const { type, payload } = message;

    if (type === 'offer') {
        await peerConnection.setRemoteDescription(new RTCSessionDescription(payload));
        const answer = await peerConnection.createAnswer();
        await peerConnection.setLocalDescription(answer);
        sendMessage('answer', answer);
    } else if (type === 'answer') {
        await peerConnection.setRemoteDescription(new RTCSessionDescription(payload));
    } else if (type === 'candidate') {
        await peerConnection.addIceCandidate(new RTCIceCandidate(payload));
    }
}

// WebSocket or other method to receive messages from the server
// Example: socket.onmessage = (event) => handleMessage(JSON.parse(event.data));