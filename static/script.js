document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const imageUpload = document.getElementById('imageUpload');
    const uploadArea = document.getElementById('uploadArea');
    const resultArea = document.getElementById('resultArea');
    const resultBox = document.getElementById('resultBox');
    const diseaseName = document.getElementById('diseaseName');
    const confidence = document.getElementById('confidence');
    const previewImage = document.getElementById('previewImage');
    const resetButton = document.getElementById('resetButton');
    const loader = document.getElementById('loader');
    const treatmentBox = document.getElementById('treatmentBox'); // ✅ treatment div in HTML

    // Handle form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        if (!imageUpload.files[0]) {
            alert('Please select an image first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', imageUpload.files[0]);

        // Show loader
        loader.style.display = 'block';
        resultBox.style.display = 'none';
        treatmentBox.style.display = 'none';

        try {
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            loader.style.display = 'none'; // hide loader

            if (data.status === 'success' || data.status === 'uncertain') {
                // Show result area
                uploadArea.style.display = 'none';
                resultArea.style.display = 'block';
                
                // Display image preview
                previewImage.src = URL.createObjectURL(imageUpload.files[0]);
                
                // Display results
                diseaseName.textContent = data.prediction;
                confidence.textContent = data.confidence + '%';
                
                // ✅ Show treatment info
                treatmentBox.textContent = data.treatment || "No treatment information available.";
                treatmentBox.style.display = 'block';

                // Show result box
                resultBox.style.display = 'block';
            } else {
                throw new Error(data.error || 'Possibly not a plant image');
            }
        } catch (error) {
            loader.style.display = 'none';
            alert('Error: ' + error.message);
        }
    });

    // Reset button functionality
    resetButton.addEventListener('click', function() {
        uploadArea.style.display = 'block';
        resultArea.style.display = 'none';
        uploadForm.reset();
        treatmentBox.style.display = 'none';
    });

    // Drag and drop functionality
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', function() {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        imageUpload.files = e.dataTransfer.files;
    });
});
