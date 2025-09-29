// Demo functionality
document.addEventListener('DOMContentLoaded', function() {
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const resultArea = document.getElementById('resultArea');
    const resultImage = document.getElementById('resultImage');
    const resetButton = document.getElementById('resetButton');
    
    // Upload area click event
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    // File input change event
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            const reader = new FileReader();
            
            reader.onload = function(event) {
                // Show loading state
                uploadArea.innerHTML = '<i class="fas fa-spinner fa-spin"></i><div class="upload-text"><h3>Analyzing Image...</h3><p>Please wait while we process your image</p></div>';
                uploadArea.classList.add('active');
                
                // Simulate processing delay
                setTimeout(function() {
                    // Set the result image
                    resultImage.src = event.target.result;
                    
                    // Show result area
                    resultArea.style.display = 'block';
                    
                    // Reset upload area
                    resetUploadArea();
                }, 2000);
            };
            
            reader.readAsDataURL(file);
        }
    });
    
    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('active');
    });
    
    uploadArea.addEventListener('dragleave', function() {
        uploadArea.classList.remove('active');
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('active');
        
        if (e.dataTransfer.files.length > 0) {
            fileInput.files = e.dataTransfer.files;
            const event = new Event('change');
            fileInput.dispatchEvent(event);
        }
    });
    
    // Reset button functionality
    resetButton.addEventListener('click', resetDemo);
});

function resetUploadArea() {
    const uploadArea = document.getElementById('uploadArea');
    uploadArea.innerHTML = `
        <i class="fas fa-cloud-upload-alt"></i>
        <div class="upload-text">
            <h3>Upload Plant Image</h3>
            <p>Drag & drop or click to browse</p>
        </div>
        <p>Supported formats: JPG, PNG, JPEG (Max 5MB)</p>
        <input type="file" class="file-input" id="fileInput" accept="image/*">
    `;
    
    // Reattach event listeners
    const fileInput = document.getElementById('fileInput');
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const file = e.target.files[0];
            const reader = new FileReader();
            
            reader.onload = function(event) {
                uploadArea.innerHTML = '<i class="fas fa-spinner fa-spin"></i><div class="upload-text"><h3>Analyzing Image...</h3><p>Please wait while we process your image</p></div>';
                uploadArea.classList.add('active');
                
                setTimeout(function() {
                    document.getElementById('resultImage').src = event.target.result;
                    document.getElementById('resultArea').style.display = 'block';
                    resetUploadArea();
                }, 2000);
            };
            
            reader.readAsDataURL(file);
        }
    });
}

function resetDemo() {
    document.getElementById('resultArea').style.display = 'none';
    document.getElementById('fileInput').value = '';
}

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