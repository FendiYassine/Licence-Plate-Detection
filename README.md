# Licence Plate Detection

A Python-based License Plate Detection system for identifying and localizing license plates in images or video streams.

## Features

- Detect license plates in images or videos.
- Supports batch processing of multiple images.
- Easy to integrate with vehicle management systems.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. You can download it from [python.org](https://www.python.org/).

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/FendiYassine/Licence-Plate-Detection.git
   cd Licence-Plate-Detection
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Detect License Plates in Images

1. Place your images in the `data/test_images/` directory.
2. Run the script:
   ```bash
   python detect.py --input data/test_images/ --output results/
   ```

#### Real-Time Detection

Run the following command to detect license plates from a webcam or a video file:
   ```bash
   python detect_realtime.py --source <camera_id_or_video_path>
   ```

### Configuration

Update the `config.json` file to configure:
- Input/output directories
- Detection parameters

## Folder Structure

```
Licence-Plate-Detection/
├── data/
│   ├── test_images/       # Input images for testing
├── results/               # Output directory for results
├── weights/               # Pre-trained weights
├── detect.py              # Detection script for images
├── detect_realtime.py     # Real-time detection script
├── config.json            # Configuration file
├── requirements.txt       # Required Python packages
├── README.md              # Project documentation
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.
