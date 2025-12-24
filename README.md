# 🍎🍌🍊 Fruit Recognition System

<div align="center">
  <img src="static/images/fruity-detect-logo.png" alt="Fruity Detect Logo" width="200"/>
  
  [![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
  [![Flask](https://img.shields.io/badge/framework-Flask-lightgrey.svg)](https://flask.palletsprojects.com/)
  [![OpenCV](https://img.shields.io/badge/OpenCV-4.12.0-green.svg)](https://opencv.org/)
  [![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6+-orange.svg)](https://scikit-learn.org/)
  
  📊 **Dataset**: [Fruits-360](https://www.kaggle.com/datasets/moltean/fruits)
</div>

A web-based fruit classification system that uses classical computer vision and machine learning to identify fruits from images. The system can classify **230 different fruit types** from the Fruits-360 dataset. Users can upload fruit images through a web interface and receive real-time predictions with confidence scores. The system follows a classical computer vision pipeline that processes images through multiple stages before classification.

## Demo

### Overview

<!-- Add your overview GIF/video here -->

### Predictions

<!-- Add your predictions GIF/video here -->

## How It Works

The system follows a **6-stage classical computer vision pipeline**:

<div align="center">
  <img src="static/images/fruit-recognition-pipeline.png" alt="Fruit Recognition Pipeline" width="800"/>
</div>

### 1. Image Acquisition & Loading
The process begins when a user uploads a fruit image through the web interface. The image is loaded and prepared for processing.

### 2. Color Space Conversion (HSV)
The uploaded image is converted from RGB/BGR color space to **HSV (Hue, Saturation, Value)** color space. This conversion separates the image into three channels:
- **Hue**: Represents the color type (0-360 degrees)
- **Saturation**: Represents the color intensity (0-255)
- **Value**: Represents the brightness (0-255)

### 3. Image Segmentation (Thresholding)
The saturation channel is used to create a binary mask that isolates the fruit region from the background. A threshold value of 15 is applied: pixels with saturation greater than 15 are considered part of the fruit, while others are treated as background. This creates a segmented mask that identifies the fruit pixels.

### 4. Image Description & Feature Extraction
From the segmented fruit region, **4 key features** are extracted:
- **Area**: The number of pixels in the fruit region (fruit size)
- **Average Hue**: Circular mean of hue values for fruit pixels only (color characteristic)
- **Average Saturation**: Mean saturation value for fruit pixels (color intensity)
- **Average Value**: Mean brightness value for fruit pixels (brightness characteristic)

These features form a compact representation of the fruit's visual properties.

### 5. Data Preparation & Preprocessing
The extracted features undergo two key preprocessing steps:
- **Feature Normalization**: Features are normalized using a **MinMaxScaler** that was fitted during model training. This ensures the feature values are scaled to the same range (0-1) as the training data, which is essential for accurate predictions.
- **Label Encoding**: Fruit class names are encoded into numerical labels using a **LabelEncoder** that maps each fruit type to a unique integer. During prediction, the model outputs an encoded numerical label, which is then decoded back to the original fruit name using the inverse transformation.

### 6. Object Recognition & Classification
The normalized feature vector is fed into a trained **Random Forest classifier** that predicts the fruit type. The model returns both the predicted fruit class and a confidence score indicating the prediction certainty.

## Features

- 🖼️ Interactive web interface for image upload
- 🎯 Real-time fruit classification
- 📊 Confidence score display
- 🎨 Modern, responsive UI
- 🔬 Classical computer vision approach (no deep learning)

## Dataset

Trained on the [Fruits-360 Dataset](https://www.kaggle.com/datasets/moltean/fruits) from Kaggle, which contains images of 230 different fruit types.

## Setup Instructions

### To set up your environment after cloning (from the project root):

**1. Create a virtual environment:**
```bash
python -m venv .venv
```

**2. Activate the virtual environment:**

```bash
.venv\Scripts\activate
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Ensure you have the trained model file:**
Make sure `fruit_model.joblib` is present in the project root directory.
**Note:** The model file (~2GB) is not included in the repository due to size limitations. You'll need to generate it using the training notebook (`Fruit_Recognition.ipynb`) or obtain it separately.

**5. Run the Flask application:**
```bash
python app.py
```

**6. Access the application:**
Open your browser and navigate to:
```
http://localhost:3000
```
