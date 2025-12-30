import os, warnings
from flask import Flask, request, jsonify, render_template
import joblib
from PIL import Image
import numpy as np
import cv2
from scipy.stats import circmean

# Suppress sklearn version warnings
warnings.filterwarnings('ignore', category=UserWarning, module='sklearn')

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model bundle
# The model bundle contains: 'model', 'scaler', 'label_encoder'
model_path = "fruit_model.joblib"
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # Access the model file on disk as if it were in memory, without loading the entire file into RAM at once. (For deployment purposes)
    model_bundle = joblib.load(model_path, mmap_mode='r')

# Extract components from the bundle
rf_model = model_bundle['model']
minmax_scaler = model_bundle['scaler']
label_encoder = model_bundle['label_encoder']

# Function to segment fruit (convert BGR to HSV and create binary mask)
def segment_fruit(image_bgr):
    # Convert the BGR image to HSV color space
    image_hsv = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2HSV)
    
    # Split into individual channels (returns numpy arrays)
    hue, saturation, value = cv2.split(image_hsv)
    
    # Segment the image through simple global thresholding on saturation channel
    # Threshold value of 15: pixels with saturation > 15 are considered fruit
    _, segmented_mask = cv2.threshold(saturation, 15, 255, cv2.THRESH_BINARY)
    
    return hue, saturation, value, segmented_mask

# Function to extract features from segmented fruit
def extract_features(hue, saturation, value, segmented_mask):
    # 1. Area: Count of white pixels in the mask (fruit region size)
    area = np.count_nonzero(segmented_mask)
    
    # Filter only fruit pixels using the mask
    # Utilize numpy's masking feature: filters True values, removes False values
    fruit_hue = hue[segmented_mask == 255]
    fruit_saturation = saturation[segmented_mask == 255]
    fruit_value = value[segmented_mask == 255]
    
    # 2. Average Hue: Use circular mean because hue is circular (0-360 degrees)
    # Multiply by 2 and divide by 2 to handle circular statistics correctly
    avg_hue = circmean(fruit_hue * 2, high=360, low=0) / 2
    
    # 3. Average Saturation: Mean of saturation values for fruit pixels only
    avg_saturation = np.mean(fruit_saturation)
    
    # 4. Average Value: Mean of value (brightness) for fruit pixels only
    avg_value = np.mean(fruit_value)
    
    # Return feature vector as list
    return [int(area), float(avg_hue), float(avg_saturation), float(avg_value)]

# Function to preprocess image for prediction - the whole Image Processing pipelinehappens here
def preprocess_image(image):
    """
    Preprocesses a PIL Image for model prediction.
    
    Args:
        image: PIL Image object
    
    Returns:
        Normalized feature array ready for model prediction
    """
    # Convert PIL Image to numpy array (RGB format)
    image_rgb = np.array(image)
    
    # Convert RGB to BGR (OpenCV uses BGR format)
    image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)
    
    # Segment the fruit to get HSV channels and mask
    hue, saturation, value, mask = segment_fruit(image_bgr)
    
    # Extract features from the segmented fruit
    features = extract_features(hue, saturation, value, mask)
    
    # Convert to numpy array and reshape for single sample
    # Why reshape? extract_features() returns a 1D list (4 elements)
    # Scikit-learn's predict() expects 2D array: (n_samples, n_features)
    # For a single prediction, we need shape (1, 4) not (4,)
    # reshape(1, -1) means: 1 row, auto-calculate columns (which will be 4)
    features_array = np.array(features).reshape(1, -1)
    
    # Normalize features using the SAME scaler from training
    # Important: Use .transform(), NOT .fit_transform() to use training statistics
    features_normalized = minmax_scaler.transform(features_array)
    
    return features_normalized

# Home page route
@app.route("/", methods=["GET"])
def home():
    """Render the home page with the fruit recognition interface."""
    return render_template("index.html")

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    """
    Handles fruit image prediction requests.
    
    Expects:
        - POST request with 'fruitImage' file in form data
    
    Returns:
        - JSON response with 'prediction' (fruit name) on success
        - JSON response with 'error' message on failure
    """
    try:
        # Check if file is present in the request
        if 'fruitImage' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        # Get the uploaded file
        file = request.files['fruitImage']
        
        # Check if file was actually selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Open the image file using PIL
        image = Image.open(file.stream)
        
        # Preprocess the image (returns normalized features)
        features_normalized = preprocess_image(image)
        
        # Make the prediction (returns encoded label number)
        # prediction_encoded = rf_model.predict(features_normalized)[0]
        # .predict(): Returns only the predicted class label (the class with the highest probability).
        
        # .predict_proba(): Returns the probabilities for all classes (the probability of each class being the predicted class).
        # Get prediction probabilities for all classes
        prediction_proba = rf_model.predict_proba(features_normalized)[0]
        
        # Get the predicted class (highest probability)
        prediction_encoded = np.argmax(prediction_proba)
        
        # Get the confidence score (probability of the predicted class)
        confidence_score = float(prediction_proba[prediction_encoded])
        
        # Decode the prediction to get the fruit name
        # The model returns an encoded number, we need to convert it back to the fruit name
        prediction_label = label_encoder.inverse_transform([prediction_encoded])[0]
        
        # Return the prediction and confidence score as a JSON response
        return jsonify({
            'prediction': prediction_label,
            'confidence': confidence_score
        })
    
    except Exception as e:
        # Return JSON error response for better debugging
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# Run the Flask app on port 3000
if __name__ == "__main__":
    app.run(port=3000, debug=True)
