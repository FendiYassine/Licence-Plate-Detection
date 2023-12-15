from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess
import pytesseract
from PIL import Image
import pandas as pd
# import pytesseract
import easyocr
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Adjust the path accordingly

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def run_inference(file_path):
    # Run YOLOv5 inference using detect.py script
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    output_path = os.path.join(output_dir, 'temp.jpg')  # Use 'temp.jpg' as the file name
    temp_txt_path = os.path.join(output_dir, 'labels', 'temp.txt')  # Path to temp.txt

    # Remove existing temp.txt file
    if os.path.exists(temp_txt_path):
        os.remove(temp_txt_path)

    command = [
        "python",
        r"C:\Users\torjm\OneDrive\Bureau\licence plate\license-plate-ocr\yolov5\detect.py",
        "--weights",
        r"C:\Users\torjm\OneDrive\Bureau\licence plate\license-plate-ocr\yolov5\runs\train\results_5\weights\best.pt",
        "--img-size",
        "640",
        "--conf",
        "0.5",  # Set confidence threshold as needed
        "--source",
        file_path,
        "--save-txt",
        "--save-conf",
        "--exist-ok",
        "--project",
        output_dir,
        "--name",
        "result"
    ]

    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
        print('Inference completed successfully')
        return output_path
    except subprocess.CalledProcessError as e:
        print('Error during inference:', e)
        return {"error": str(e)}

def crop_image(image_path, x1, y1, x2, y2):
    # Crop the image using PIL
    print(image_path)
    image = Image.open(image_path)
    cropped_image = image.crop((x1, y1, x2, y2))
    cropped_image_path = 'output/cropped.jpg'
    cropped_image.save(cropped_image_path)
    return cropped_image_path

def extract_bounding_box_from_yolo_output(output_path, image_width, image_height):
    # Extract bounding box coordinates from YOLOv5 output
    with open(output_path, 'r') as f:
        lines = f.readlines()
        values = lines[0].split(' ')[1:6]  # Corrected the index range
        x_center, y_center, width_percent, height_percent, _ = map(float, values)

        # Convert percentages to actual values
        width = width_percent * image_width
        height = height_percent * image_height

        return x_center, y_center, width, height


        


def perform_ocr():
    image_path = 'C:\\Users\\torjm\\OneDrive\\Bureau\\licence plate\\license-plate-ocr\\output\\result\\temp.jpg'
    image = Image.open(image_path)
    image_width, image_height = image.size
    x1, y1, width, height = extract_bounding_box_from_yolo_output('C:\\Users\\torjm\\OneDrive\\Bureau\\licence plate\\license-plate-ocr\\output\\result\\labels\\temp.txt', image_width, image_height)
    print('as you see', x1, y1, width, height)
    
    # Crop the image using bounding box coordinates
    cropped_image_path = crop_image(image_path, int(x1), int(y1), int(x1 +width), int(y1+ height))
    
    print('ena*******', cropped_image_path)
    
    reader = easyocr.Reader(['en'])  # You can add more languages if needed
    result = reader.readtext(cropped_image_path)
    extracted_text = ' '.join([entry[1] for entry in result])

    return extracted_text


def save_to_excel(extracted_text):  
    # Save extracted text to an Excel file

    df = pd.DataFrame({'Extracted Information': [extracted_text]})
    excel_path = 'C:\\Users\\torjm\OneDrive\\Bureau\\licence plate\\license-plate-ocr\\output\\extracted_information.xlsx'
    df.to_excel(excel_path, index=False)
    return excel_path

@app.route('/upload', methods=['POST'])
def upload_file():
    # Handle file upload
    file = request.files['file']

    # Save the file to a temporary location
    save_dir = 'uploads'
    os.makedirs(save_dir, exist_ok=True)  # Create the directory if it doesn't exist
    file_path = os.path.join(save_dir, 'temp.jpg')
    file.save(file_path)

    # Run YOLOv5 inference
    result_image_path = run_inference(file_path)
    print("Result Image Path:", result_image_path)

    # Perform OCR on the cropped image
    extracted_text = perform_ocr()

    # Save extracted information to an Excel file
    excel_path = save_to_excel(extracted_text)

    return jsonify({
        'message': 'File uploaded successfully',
        'result_image_path': result_image_path,
        'extracted_text': extracted_text,
        'excel_path': excel_path
    })

@app.route('/output/result/<filename>')
def result_image(filename):
    return send_from_directory(os.path.join('C:\\Users\\torjm\\OneDrive\\Bureau\\licence plate\\license-plate-ocr', 'output/result'), filename, mimetype='image/jpeg')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)


if __name__ == '__main__':
    app.run(debug=True)
