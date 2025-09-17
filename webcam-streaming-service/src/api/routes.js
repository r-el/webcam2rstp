const express = require('express');
const router = express.Router();
const { startStream, stopStream } = require('../stream/camera');

// Route to start the video stream
router.post('/start', (req, res) => {
    startStream()
        .then(() => res.status(200).json({ message: 'Stream started' }))
        .catch(err => res.status(500).json({ error: err.message }));
});

// Route to stop the video stream
router.post('/stop', (req, res) => {
    stopStream()
        .then(() => res.status(200).json({ message: 'Stream stopped' }))
        .catch(err => res.status(500).json({ error: err.message }));
});

module.exports = router;