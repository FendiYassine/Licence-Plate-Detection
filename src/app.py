from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import subprocess
from PIL import Image
import pandas as pd
import easyocr
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

def run_inference(file_path):
    # Run YOLOv5 inference using detect.py script
    output_dir = 'output'
    os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist
    output_path = os.path.join(output_dir, 'temp.jpg')  # Use 'temp.jpg' as the file name
    temp_txt_path = os.path.join(output_dir, 'result/labels', 'temp.txt')  # Path to temp.txt

    if os.path.exists(temp_txt_path):
        with open(temp_txt_path, 'w') as f:
            f.write('')  # Clear the content of temp.txt

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



def crop_image(image_path, x_center, y_center, width_percent, height_percent):
    # Open the image using PIL
    image = Image.open(image_path)
    img_width, img_height = image.size
    Image.MAX_IMAGE_PIXELS = None

    # Convert YOLO bounding box (normalized values) to PIL format (pixel values)
    left = img_width * (x_center - width_percent / 2.)
    right = img_width * (x_center + width_percent / 2.)
    upper = img_height * (y_center - height_percent / 2.)
    lower = img_height * (y_center + height_percent / 2.)

    # Crop the image
    cropped_image = image.crop((left, upper, right, lower))
    cropped_image_path = 'output/cropped.jpg'
    cropped_image.save(cropped_image_path)
    return cropped_image_path

def extract_bounding_box_from_yolo_output(output_path):
    # Extract bounding box coordinates from YOLOv5 output
    with open(output_path, 'r') as f:
        lines = f.readlines()
        values = lines[0].split(' ')[1:5]
        x_center, y_center, width_percent, height_percent = map(float, values)
        return x_center, y_center, width_percent, height_percent

def perform_ocr():
    image_path = 'C:\\Users\\torjm\\OneDrive\\Bureau\\licence plate\\license-plate-ocr\\output\\result\\temp.jpg'
    x_center, y_center, width_percent, height_percent = extract_bounding_box_from_yolo_output('C:\\Users\\torjm\\OneDrive\\Bureau\\licence plate\\license-plate-ocr\\output\\result\\labels\\temp.txt')

    # Crop the image using bounding box coordinates
    cropped_image_path = crop_image(image_path, x_center, y_center, width_percent, height_percent)

    print('Cropped image path:', cropped_image_path)

    # Configure OCR to detect English alphabet and digits
    reader = easyocr.Reader(['en'])
    result = reader.readtext(cropped_image_path)
    extracted_text = ' '.join([entry[1] for entry in result])

    return extracted_text


def save_to_excel(extracted_text):
    # Save extracted text to an Excel file
    excel_path = 'C:\\Users\\torjm\\OneDrive\\Bureau\\licence plate\\license-plate-ocr\\output\\extracted_information.xlsx'

    # Check if the file exists
    if os.path.exists(excel_path):
        # If the file exists, read the existing data
        df = pd.read_excel(excel_path)
    else:
        # If the file does not exist, create a new DataFrame
        df = pd.DataFrame()

    # Append the new data
    new_data = pd.DataFrame({'Extracted Information': [extracted_text]})
    df = pd.concat([df, new_data], ignore_index=True)

    # Write the DataFrame back to the Excel file
    df.to_excel(excel_path, index=False)

    return excel_path


def clear_temp_txt():
    temp_txt_path = 'C:\\Users\\torjm\\OneDrive\\Bureau\\licence plate\\license-plate-ocr\\output\\result\\labels\\temp.txt'
    
    # Check if the file exists
    if not os.path.exists(temp_txt_path):
        # If the file does not exist, create it
        open(temp_txt_path, 'w').close()

    # Now the file should always exist
    with open(temp_txt_path, 'w') as f:
        f.write('')  # Clear the content of temp.txt
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

    # Clear the content of temp.txt
    clear_temp_txt()

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
