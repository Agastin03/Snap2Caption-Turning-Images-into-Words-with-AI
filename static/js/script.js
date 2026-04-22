// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const previewSection = document.getElementById('previewSection');
const imagePreview = document.getElementById('imagePreview');
const captionText = document.getElementById('captionText');
const copyBtn = document.getElementById('copyBtn');
const regenerateBtn = document.getElementById('regenerateBtn');
const newImageBtn = document.getElementById('newImageBtn');
const errorMessage = document.getElementById('errorMessage');
const captionStyle = document.getElementById('captionStyle');
const detailLevel = document.getElementById('detailLevel');
const detailValue = document.getElementById('detailValue');

let currentFile = null;

// Update detail level display
detailLevel.addEventListener('input', (e) => {
    const levels = ['Brief', 'Medium', 'Detailed'];
    detailValue.textContent = levels[e.target.value - 1];
});

// Upload area click
uploadArea.addEventListener('click', () => {
    fileInput.click();
});

// Drag and drop events
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    handleFile(file);
});

// File input change
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    handleFile(file);
});

// Handle file selection
function handleFile(file) {
    hideError();

    if (!file) return;

    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showError('Please upload a valid image file (PNG, JPG, JPEG, or WEBP)');
        return;
    }

    // Validate file size (5MB)
    if (file.size > 5 * 1024 * 1024) {
        showError('File size must be less than 5MB');
        return;
    }

    currentFile = file;

    // Preview image
    const reader = new FileReader();
    reader.onload = (e) => {
        imagePreview.src = e.target.result;
        previewSection.style.display = 'block';
        
        // Scroll to preview
        setTimeout(() => {
            previewSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 100);
        
        // Generate caption
        generateCaption();
    };
    reader.readAsDataURL(file);
}

// Generate caption
async function generateCaption() {
    if (!currentFile) return;

    // Show loading state
    captionText.innerHTML = `
        <div class="loading">
            <div class="spinner"></div>
            <span>Generating caption...</span>
        </div>
    `;
    copyBtn.style.display = 'none';
    regenerateBtn.style.display = 'none';

    // Prepare form data
    const formData = new FormData();
    formData.append('image', currentFile);
    formData.append('style', captionStyle.value);
    formData.append('detail', detailLevel.value);

    try {
        const response = await fetch('/generate-caption', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || 'Failed to generate caption');
        }

        // Display caption
        captionText.textContent = data.caption;
        copyBtn.style.display = 'inline-block';
        regenerateBtn.style.display = 'inline-block';

    } catch (error) {
        console.error('Error:', error);
        captionText.innerHTML = '<span style="color: #c33;">Failed to generate caption. Please try again.</span>';
        showError(error.message || 'An error occurred while generating the caption');
    }
}

// Copy caption to clipboard
copyBtn.addEventListener('click', async () => {
    const text = captionText.textContent;
    try {
        await navigator.clipboard.writeText(text);
        const originalText = copyBtn.textContent;
        const originalBg = copyBtn.style.background;
        
        copyBtn.textContent = '✓ Copied!';
        copyBtn.style.background = '#38a169';
        
        setTimeout(() => {
            copyBtn.textContent = originalText;
            copyBtn.style.background = originalBg;
        }, 2000);
    } catch (err) {
        showError('Failed to copy to clipboard');
    }
});

// Regenerate caption
regenerateBtn.addEventListener('click', () => {
    generateCaption();
});

// Upload new image
newImageBtn.addEventListener('click', () => {
    fileInput.value = '';
    currentFile = null;
    previewSection.style.display = 'none';
    hideError();
    
    // Scroll to upload area
    setTimeout(() => {
        uploadArea.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 100);
});

// Show error message
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        hideError();
    }, 5000);
}

// Hide error message
function hideError() {
    errorMessage.style.display = 'none';
}

// Auto-hide alerts after 5 seconds
document.addEventListener('DOMContentLoaded', () => {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
});
