const { getUserMedia } = require('navigator.mediaDevices');

class Camera {
    constructor() {
        this.stream = null;
    }

    async start() {
        try {
            this.stream = await getUserMedia({ video: true });
            return this.stream;
        } catch (error) {
            console.error('Error accessing the camera: ', error);
            throw error;
        }
    }

    stop() {
        if (this.stream) {
            const tracks = this.stream.getTracks();
            tracks.forEach(track => track.stop());
            this.stream = null;
        }
    }
}

module.exports = Camera;