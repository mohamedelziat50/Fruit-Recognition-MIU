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

fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    
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

// Predict button functionality
predictBtn.addEventListener('click', function() {
    if (fileInput.files.length === 0) {
        alert('Please select an image first!');
        return;
    }
});
