// DOM Elements
const uploadSection = document.getElementById('uploadSection');
const fileInput = document.getElementById('fileInput');
const analyzeBtn = document.getElementById('analyzeBtn');
const loading = document.getElementById('loading');
const results = document.getElementById('results');
const errorDiv = document.getElementById('error');
const fileInfo = document.getElementById('fileInfo');
const summary = document.getElementById('summary');
const keyPoints = document.getElementById('keyPoints');

let selectedFile = null;

// Click to upload
uploadSection.addEventListener('click', () => {
    fileInput.click();
});

// File selection
fileInput.addEventListener('change', (e) => {
    handleFileSelect(e.target.files[0]);
});

// Drag and drop
uploadSection.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadSection.classList.add('dragging');
});

uploadSection.addEventListener('dragleave', () => {
    uploadSection.classList.remove('dragging');
});

uploadSection.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadSection.classList.remove('dragging');
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFileSelect(files[0]);
    }
});

// Handle file selection
function handleFileSelect(file) {
    // Validate file
    if (!file) {
        return;
    }
    
    if (!file.name.endsWith('.pdf')) {
        showError('Please select a PDF file');
        return;
    }
    
    if (file.size > 10 * 1024 * 1024) { // 10MB limit
        showError('File size exceeds 10MB limit');
        return;
    }
    
    selectedFile = file;
    
    // Show file info
    fileInfo.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
    fileInfo.classList.add('active');
    
    // Enable analyze button
    analyzeBtn.disabled = false;
    
    // Hide error if any
    errorDiv.classList.remove('active');
    
    // Hide results from previous analysis
    results.classList.remove('active');
}

// Analyze button click
analyzeBtn.addEventListener('click', async () => {
    if (!selectedFile) {
        showError('Please select a file first');
        return;
    }
    
    await analyzeDocument();
});

// Analyze document
async function analyzeDocument() {
    // Show loading
    loading.classList.add('active');
    analyzeBtn.disabled = true;
    errorDiv.classList.remove('active');
    results.classList.remove('active');
    
    try {
        // Create form data
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        // Send request
        const response = await fetch('/api/analyze', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        // Hide loading
        loading.classList.remove('active');
        
        if (response.ok && data.success) {
            // Show results
            displayResults(data);
        } else {
            // Show error
            showError(data.message || 'Failed to analyze document');
            analyzeBtn.disabled = false;
        }
        
    } catch (error) {
        loading.classList.remove('active');
        showError('Network error: ' + error.message);
        analyzeBtn.disabled = false;
    }
}

// Display results
function displayResults(data) {
    // Set summary
    summary.textContent = data.summary;
    
    // Set key points
    keyPoints.innerHTML = '';
    if (data.key_points && data.key_points.length > 0) {
        data.key_points.forEach(point => {
            const li = document.createElement('li');
            li.textContent = point;
            keyPoints.appendChild(li);
        });
    } else {
        keyPoints.innerHTML = '<li>No key points extracted</li>';
    }
    
    // Show results
    results.classList.add('active');
    
    // Scroll to results
    results.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Show error
function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.add('active');
    
    // Auto hide after 5 seconds
    setTimeout(() => {
        errorDiv.classList.remove('active');
    }, 5000);
}

// Format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
}
