# Major_Project
# **Diabetic Retinopathy Detection System**

![Diabetic Retinopathy Detection](https://github.com/Ritiksb007/Major_Project/blob/Documentation/UI.png)  
*An AI-powered solution for early detection and classification of Diabetic Retinopathy (DR).*

---

## **Overview**  
Diabetic Retinopathy (DR) is a leading cause of vision impairment and blindness, necessitating early and accurate diagnosis to prevent severe complications. This project leverages deep learning, specifically MobileNetV2, to develop an efficient, accessible, and reliable tool for detecting DR and assessing its severity.  

The system supports:  
- **Binary Classification**: Identifying whether an image has DR or not.  
- **Multiclass Classification**: Classifying DR severity into four stages: Mild, Moderate, Proliferative_DR, and Severe.  

This project is designed for healthcare professionals and integrates seamlessly into clinical workflows, supporting telemedicine and mobile health initiatives. The model is deployed on **Hugging Face**, making it easily accessible for inference.

---

## **Features**  
- **High Accuracy**: MobileNetV2 ensures precise classification of DR severity.  
- **Web-Based Deployment**: The model is hosted on Hugging Face, offering easy accessibility.  
- **Real-Time Predictions**: Processes and classifies images in seconds.  
- **Lightweight Design**: MobileNetV2 is optimized for low-resource systems, ensuring scalability.  
- **Telemedicine Integration**: Supports remote DR screening for underserved and rural populations.  

---

## **Technologies Used**  
- **Programming Language**: Python  
- **Frameworks and Tools**:  
  - TensorFlow/Keras for deep learning  
  - Flask for backend (if applicable for local deployment)  
  - Hugging Face for model hosting  
- **Model Architecture**: MobileNetV2 with transfer learning  

---

## **Datasets Used**  
1. **APTOS 2019 Blindness Detection**  
   - 3,663 fundus images labeled with DR severity, resized to 224x224 pixels.  
2. **Diabetic Retinopathy Detection (2015 Data Colored Resized)**  
   - 35,126 resized images for multiclass classification.  

---

## **Deployment on Hugging Face**  

The trained MobileNetV2 model for both binary and multiclass classification tasks is deployed on **Hugging Face**. Access the model via the following links:  

- **Binary Classifier**: [Hugging Face Binary Classifier](#)  
- **Multiclass Classifier**: [Hugging Face Multiclass Classifier](#)  

Use the Hugging Face inference API to upload images and receive classification results in real-time.

---

## **Usage Instructions**  
1. Access the deployed model on Hugging Face through the provided links.  
2. Upload retinal fundus images for DR detection.  
3. Choose the desired classification type: binary or multiclass.  
4. View the results, including DR presence or severity level, in seconds.  

---

## **Model Performance**  

### **Binary Classification Results**  
- **Training Accuracy**: 99.42%  
- **Validation Accuracy**: 95.10%  

### **Multiclass Classification Results**  
- **Training Accuracy**: 98%  
- **Validation Accuracy**: 98.88%  

The system demonstrates high reliability and accuracy in both binary and multiclass DR classification tasks.

---

## **System Architecture**  
![System Architecture](https://github.com/Ritiksb007/Major_Project/blob/Documentation/Final%20System%20Architecture.png)

---
acknowledge the contributions of the deep learning frameworks, such as TensorFlow and Keras, which provided the necessary tools for building and deploying this project. Special thanks to the Hugging Face platform for offering a robust model hosting and inference API that facilitated seamless deployment.

---

## **How to Contribute**  
We welcome contributions to enhance this project! Here’s how you can get involved:  
1. **Fork the Repository**:  
   - Click the **Fork** button on the top right of this page to create a copy of the repository in your GitHub account.  
2. **Clone the Fork**:  
   ```bash
   git clone https://github.com/your-username/diabetic-retinopathy-detection.git
   cd diabetic-retinopathy-detection

## **Project Structure**  
```plaintext
diabetic-retinopathy-detection/
│
├── datasets/          # Dataset files
├── models/            # Trained models
├── static/            # Static files (if applicable for local deployment)
├── templates/         # HTML templates (if applicable for local deployment)
├── app.py             # Flask application (for local deployment)
├── README.md          # Project documentation
├── requirements.txt   # Python dependencies
└── ... (other files)
