import os
from flask import Flask, request, jsonify, render_template
import joblib
from PIL import Image
import numpy as np
import cv2
# from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
# CORS(app)

# Use joblib to load the trained model
model_path = "fruit_model.joblib"
model = joblib.load(model_path)

# Home page route
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")  # Render the index.html template from the templates folder

# Prediction route
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Open the image file
        fruitImage = request.files['fruitImage']
        image = Image.open(fruitImage)
        
        # Preprocess the image
        preprocessed_image = preprocess_image(image)
        
        # Make the prediction
        prediction = model.predict(preprocessed_image)[0]  # Get prediction label directly
        
        # Return the prediction as a JSON response
        return jsonify({'prediction': prediction})

    except Exception as e:
        # Return JSON error response for better debugging
        return jsonify({'error': f"An error occurred: {str(e)}"}), 500

# Run the Flask app on port 3000
if __name__ == "__main__":
    app.run(port=3000, debug=True)