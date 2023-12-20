
## Getting Started

### Prerequisites

- Python (3.x)
- Node.js and npm

### Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/FendiYassine/Licence-Plate-Detection.git
    cd licence-plate-ocr
    ```

2. Install dependencies:

    ```bash
    # Install Python dependencies
    pip install -r requirements.txt

    # Install Node.js dependencies
    npm install
    ```

### Training YOLOv5

1. Download the YOLOv5 repository:

    ```bash
    git clone https://github.com/ultralytics/yolov5.git
    ```

2. Train your YOLOv5 model using the instructions provided in the [YOLOv5 documentation](https://github.com/ultralytics/yolov5).

### Running the Local Web Page

1. Set up Flask backend:

    ```bash
    # Run Flask app
    python app.py
    ```

2. Set up React frontend:

    ```bash
    # In another terminal, go to the frontend directory
    cd frontend

    # Run React app
    npm start
    ```

3. Open your browser and navigate to `http://localhost:3000` to use the web page.

Please note : that you should change paths to avoid errors.

## Usage

1. Upload an image using the provided interface.
2. Click on the "upload" button to apply YOLOv5 on the uploaded image.
3. View the result on the web page and extracted information.
4. Check the output directory for saved information.

## Acknowledgments

- YOLOv5: https://github.com/ultralytics/yolov5
- Dataset: https://universe.roboflow.com/augmented-startups/vehicle-registration-plates-trudk

## License

This project is licensed under the [MIT License](LICENSE).
