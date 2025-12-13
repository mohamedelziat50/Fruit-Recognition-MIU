# Fruit-Recognition-MIU
Image Processing project for fruit recognition using the Fruits-360 dataset.

## Project Description
This project uses a simple computer-vision approach for fruit recognition. The fruit image is processed by converting to the saturation channel (S-channel) of the HSV color space. A binary mask is created using thresholding, which isolates the fruit region. This segmented mask is then used to extract features for classification.

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
**Note:** The model file (~2GB) is not included in the repository due to size limitations. You'll need to generate it using the training notebook or obtain it separately.

**5. Run the Flask application:**
```bash
python app.py
```

**6. Access the application:**
Open your browser and navigate to:
```
http://localhost:3000
```

## Dataset Reference
Fruits-360 Dataset: [https://www.kaggle.com/datasets/moltean/fruits](https://www.kaggle.com/datasets/moltean/fruits)