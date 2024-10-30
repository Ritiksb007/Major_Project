from flask import Flask, request, render_template, redirect, url_for, make_response
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import cv2
from werkzeug.utils import secure_filename
import os
import pdfkit

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the trained models
binary_model = load_model(r'B-DR-MobileNet2V.h5')
multi_model = load_model(r'M-DR-MobileNet2V.h5')

# Define class names
binary_class_names = np.array(['DR', 'No_DR'])
multi_class_names = np.array(['Mild', 'Moderate', 'Proliferate_Dr', 'Severe'])

def clear_uploads():
    folder = app.config['UPLOAD_FOLDER']
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

@app.route('/')
def index():
    clear_uploads()  # Clears previously uploaded images from the upload folder
    return render_template('index.html', 
                          binary_prediction=None, 
                          binary_image_path=None, 
                          show_multi_class=False, 
                          multi_prediction=None, 
                          multi_image_path=None)



def process_image(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # Preprocess the image
    image = cv2.imread(file_path)
    image_resized = cv2.resize(image, (224, 224))
    image = np.expand_dims(image_resized, axis=0)
    
    relative_path = os.path.join('uploads', filename).replace('\\', '/')
    return image, f'static/{relative_path}'

@app.route('/predict_binary', methods=['POST'])
def predict_binary():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        image, file_path = process_image(file)
        prediction = binary_model.predict(image)
        predicted_class = binary_class_names[np.argmax(prediction)]

        # Get patient details from form
        patient_details = {
            'name': request.form.get('patientName', ''),
            'age': request.form.get('patientAge', ''),
            'dob': request.form.get('patientDOB', ''),
            'gender': request.form.get('patientGender', ''),
            'incline': request.form.get('patientIncline', ''),
            'history': request.form.get('patientHistory', '')
        }

        show_multi_class = predicted_class == 'DR'
        
        return render_template('index.html', 
                              binary_prediction=predicted_class, 
                              binary_image_path=file_path,
                              show_multi_class=show_multi_class,
                              patient_details=patient_details)

@app.route('/predict_multi', methods=['POST'])
def predict_multi():
    if 'file' not in request.files:
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        return redirect(url_for('index'))

    if file:
        image, file_path = process_image(file)
        prediction = multi_model.predict(image)
        predicted_class = multi_class_names[np.argmax(prediction)]

        # Get patient details from form
        patient_details = {
            'name': request.form.get('patientName', ''),
            'age': request.form.get('patientAge', ''),
            'dob': request.form.get('patientDOB', ''),
            'gender': request.form.get('patientGender', ''),
            'incline': request.form.get('patientIncline', ''),
            'history': request.form.get('patientHistory', '')
        }

        return render_template('index.html', 
                              binary_prediction='DR',
                              binary_image_path=file_path,
                              show_multi_class=True,
                              multi_prediction=predicted_class, 
                              multi_image_path=file_path,
                              patient_details=patient_details)

@app.route('/generate_report', methods=['POST'])
def generate_report():
    # Retrieve patient details
    patient_details = {
        'name': request.form.get('patientName', 'Not provided'),
        'age': request.form.get('patientAge', 'Not provided'),
        'dob': request.form.get('patientDOB', 'Not provided'),
        'gender': request.form.get('patientGender', 'Not provided'),
        'incline': request.form.get('patientIncline', 'Not provided'),
        'history': request.form.get('patientHistory', 'Not provided')
    }

    # Debugging: Print patient details to console
    print("Patient Details:", patient_details)

    # Retrieve predictions
    binary_prediction = request.form.get('binary_prediction', 'Not available')
    multi_prediction = request.form.get('multi_prediction', 'Not available')
    
    # Retrieve image path
    image_path = request.form.get('image_path', 'Not available')

    # Create the HTML content for the report
    report_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Diabetic Retinopathy Detection Report</h1>
        
        <h2>Patient Information</h2>
        <table>
            <tr><th>Field</th><th>Information</th></tr>
            <tr><td><strong>Name</strong></td><td>{patient_details['name']}</td></tr>
            <tr><td><strong>Age</strong></td><td>{patient_details['age']}</td></tr>
            <tr><td><strong>Date of Birth</strong></td><td>{patient_details['dob']}</td></tr>
            <tr><td><strong>Gender</strong></td><td>{patient_details['gender']}</td></tr>
            <tr><td><strong>Incline Level</strong></td><td>{patient_details['incline']}</td></tr>
            <tr><td><strong>Family Diabetic History</strong></td><td>{patient_details['history']}</td></tr>
        </table>

        <h2>Diagnosis Results</h2>
        <table>
            <tr><th>Test Type</th><th>Result</th></tr>
            <tr><td><strong>Binary Prediction</strong></td><td>{binary_prediction}</td></tr>
            <tr><td><strong>Multi-class Prediction</strong></td><td>{multi_prediction}</td></tr>
        </table>

        <h2>Retinal Image</h2>
        <img src="http://127.0.0.1:5000/{image_path}" alt="Retinal Image" style="max-width:100%; height:auto;">
    </body>
    </html>
    """

    # Configure pdfkit
    config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
    
    # Convert HTML to PDF
    pdf = pdfkit.from_string(report_content, False, configuration=config)

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=report.pdf'

    return response

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True)