import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

const App = () => {
  const [file, setFile] = useState(null);
  const [resultImageUrl, setResultImageUrl] = useState(null);
  const [processingResult, setProcessingResult] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      setResultImageUrl(`http://localhost:5000/output/result/temp.jpg`);

      // Assuming 'success' or 'error' is returned by your backend
      setProcessingResult(result.success ? 'success' : 'error');
      console.log('abcdef',resultImageUrl);
    } catch (error) {
      console.error('Fetch error:', error);
      setProcessingResult('error');
      
    }
  };

  return (
    <div className="bg-light min-vh-100 d-flex flex-column">
      <header className="bg-primary text-white text-center py-3">
        <h1 className="display-4 font-weight-bold">Licence plate detection using YOLOV5</h1>
      </header>
      <div className="container my-5 flex-grow-1">
        <div className="row justify-content-center">
          <div className="col-md-6">
            <div className="card shadow">
              <div className="card-body">
                <h5 className="card-title text-center mb-4">Upload Image</h5>
                <input type="file" className="form-control mb-3" onChange={handleFileChange} />
                <button className="btn btn-primary btn-block" onClick={handleUpload}>
                  Upload
                </button>
                {resultImageUrl && (
  <div className="mt-4 text-center">
    <h2 className="card-title text-center mb-3">Result Image:</h2>
    <img src={resultImageUrl} alt="Result" />
  </div>
)}
              </div>
            </div>
          </div>
        </div>
      </div>
      <footer className="bg-dark text-white text-center py-3">
        <p>&copy; 2023 Licence plate detection by Yassine Fendi</p>
      </footer>
    </div>
  );
};

export default App;
