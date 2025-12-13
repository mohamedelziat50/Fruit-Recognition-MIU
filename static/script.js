// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Image preview functionality
const fileInput = document.getElementById('fruit-image');
const imagePreview = document.getElementById('image-preview');
const predictBtn = document.getElementById('predict-btn');

// Predict button functionality
const predictionResult = document.getElementById('prediction-result');

fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    
    // Clear previous prediction when new image is selected
    predictionResult.innerHTML = '';
    predictionResult.classList.remove('loading', 'error', 'success');
    
    if (file) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            imagePreview.innerHTML = `<img src="${e.target.result}" alt="Preview">`;
            imagePreview.classList.add('show');
        };
        
        reader.readAsDataURL(file);
    } else {
        imagePreview.classList.remove('show');
        imagePreview.innerHTML = '';
    }
});

predictBtn.addEventListener('click', async function() {
    // Check if file is selected
    if (fileInput.files.length === 0) {
        alert('Please select an image first!');
        return;
    }

    // Get the selected file
    const file = fileInput.files[0];
    
    // Create FormData to send the file
    const formData = new FormData();
    formData.append('fruitImage', file);

    // Show loading state
    predictionResult.innerHTML = 'Predicting...';
    predictionResult.classList.remove('error', 'success');
    predictionResult.classList.add('loading');
    predictBtn.disabled = true;

    try {
        // Send POST request to /predict endpoint
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        // Parse JSON response
        const data = await response.json();

        if (response.ok) {
            // Success: Display prediction with confidence score
            const confidencePercent = (data.confidence * 100).toFixed(1);
            predictionResult.innerHTML = `${data.prediction} <span style="opacity: 0.7;">(${confidencePercent}% confidence)</span>`;
            predictionResult.classList.remove('loading');
            predictionResult.classList.add('success');
            // Scroll prediction into view smoothly
            predictionResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            // Error: Display error message
            predictionResult.innerHTML = `Error: ${data.error}`;
            predictionResult.classList.remove('loading');
            predictionResult.classList.add('error');
            // Scroll prediction into view smoothly
            predictionResult.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
    } catch (error) {
        // Network or other error
        console.error('Fetch error:', error);
        predictionResult.innerHTML = 'Error: Could not connect to server.';
        predictionResult.classList.remove('loading');
        predictionResult.classList.add('error');
    } finally {
        // Re-enable button
        predictBtn.disabled = false;
    }
});
