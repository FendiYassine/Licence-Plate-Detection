// server.js

const express = require('express');
const multer = require('multer');
const { spawn } = require('child_process');

const app = express();
const port = 3001;

const storage = multer.memoryStorage();
const upload = multer({ storage: storage });

app.post('/process-image', upload.single('image'), (req, res) => {
  const imageBuffer = req.file.buffer;
  const imageBase64 = imageBuffer.toString('base64');

  // Call detect.py script with image data
  const pythonProcess = spawn('python', ['path/to/yolov5/detect.py', '--source', `data:image/png;base64,${imageBase64}`, '--weights', 'path/to/your/best.pt']);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`stdout: ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`child process exited with code ${code}`);
    if (code === 0) {
      res.json({ message: 'Image processed successfully!' });
    } else {
      res.status(500).json({ message: 'Error processing image' });
    }
  });
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
