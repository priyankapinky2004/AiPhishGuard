document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const urlForm = document.getElementById('url-form');
    const urlInput = document.getElementById('url-input');
    const checkButton = document.getElementById('check-button');
    const loader = document.getElementById('loader');
    const resultContainer = document.getElementById('result-container');
    const errorContainer = document.getElementById('error-container');
    const resultUrl = document.getElementById('result-url');
    const verdictIcon = document.getElementById('verdict-icon');
    const verdictTitle = document.getElementById('verdict-title');
    const verdictDescription = document.getElementById('verdict-description');
    const probabilityValue = document.getElementById('probability-value');
    const probabilityBar = document.getElementById('probability-bar');
    const featuresGrid = document.getElementById('features-grid');
    const checkAnother = document.getElementById('check-another');
    const detailsToggle = document.getElementById('details-toggle');
    const technicalDetails = document.getElementById('technical-details');
    const jsonResponse = document.getElementById('json-response');
    const timestamp = document.getElementById('timestamp');
    const errorMessage = document.getElementById('error-message');
    const errorDismiss = document.getElementById('error-dismiss');
    const exampleUrls = document.querySelectorAll('.example-url');

    // API endpoint
    const API_URL = '/check-url';

    // Toggle technical details
    detailsToggle.addEventListener('click', function() {
        const isVisible = technicalDetails.style.display === 'block';
        technicalDetails.style.display = isVisible ? 'none' : 'block';
        
        const toggleText = detailsToggle.querySelector('span');
        const toggleIcon = detailsToggle.querySelector('i');
        
        if (isVisible) {
            toggleText.textContent = 'Show Technical Details';
            toggleIcon.classList.remove('fa-chevron-up');
            toggleIcon.classList.add('fa-chevron-down');
        } else {
            toggleText.textContent = 'Hide Technical Details';
            toggleIcon.classList.remove('fa-chevron-down');
            toggleIcon.classList.add('fa-chevron-up');
        }
    });

    // Check another URL button
    checkAnother.addEventListener('click', function() {
        resetUI();
        urlInput.value = '';
            urlInput.focus();
        });
    });

    // Error dismiss button
    errorDismiss.addEventListener('click', function() {
        resetUI();
        urlInput.focus();
    });

    // Example URL click
    exampleUrls.forEach(example => {
        example.addEventListener('click', function() {
            urlInput.value = this.dataset.url;
            urlForm.dispatchEvent(new Event('submit'));
        });
    });

    // Form submission
    urlForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        
        if (!url) {
            showError('Please enter a URL');
            return;
        }
        
        checkUrl(url);
    });

    // Check URL function
    function checkUrl(url) {
        // Show loader
        resetUI();
        loader.style.display = 'flex';
        
        // Prepare request data
        const requestData = {
            url: url
        };
        
        // Call API
        fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            displayResults(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showError('Unable to analyze URL. Please try again.');
        });
    }

    // Display results function
    function displayResults(data) {
        // Hide loader
        loader.style.display = 'none';
        
        // Update URL display
        resultUrl.querySelector('span').textContent = data.url;
        
        // Update verdict
        const isPhishing = data.result === 'phishing';
        
        if (isPhishing) {
            verdictIcon.className = 'verdict-icon phishing';
            verdictIcon.innerHTML = '<i class="fas fa-exclamation-triangle"></i>';
            verdictTitle.textContent = 'Phishing Detected';
            verdictDescription.textContent = 'This URL has been identified as a potential phishing attempt. Exercise caution.';
        } else {
            verdictIcon.className = 'verdict-icon safe';
            verdictIcon.innerHTML = '<i class="fas fa-check-circle"></i>';
            verdictTitle.textContent = 'URL is Safe';
            verdictDescription.textContent = 'This URL appears to be legitimate and safe to visit.';
        }
        
        // Update probability
        const probability = data.probability * 100;
        probabilityValue.textContent = `${probability.toFixed(2)}%`;
        probabilityBar.style.width = `${probability}%`;
        
        // Set color based on probability
        if (probability < 20) {
            probabilityBar.style.backgroundColor = 'var(--success-color)';
        } else if (probability < 60) {
            probabilityBar.style.backgroundColor = 'var(--warning-color)';
        } else {
            probabilityBar.style.backgroundColor = 'var(--danger-color)';
        }
        
        // Update features grid
        featuresGrid.innerHTML = '';
        
        const featureLabels = {
            'url_length': 'URL Length',
            'contains_ip': 'Contains IP Address',
            'num_special_chars': 'Special Characters',
            'num_subdomains': 'Subdomains',
            'has_https': 'Uses HTTPS',
            'suspicious_words': 'Suspicious Words',
            'domain_age': 'Domain Age (years)',
            'redirect_count': 'Redirect Count'
        };
        
        for (const [key, value] of Object.entries(data.features)) {
            const label = featureLabels[key] || key;
            let displayValue = value;
            let iconHtml = '';
            
            // Format boolean values
            if (key === 'contains_ip' || key === 'has_https') {
                if (value === 1) {
                    displayValue = 'Yes';
                    iconHtml = key === 'has_https' ? 
                        '<i class="fas fa-check text-success"></i>' : 
                        '<i class="fas fa-times text-danger"></i>';
                } else {
                    displayValue = 'No';
                    iconHtml = key === 'has_https' ? 
                        '<i class="fas fa-times text-danger"></i>' : 
                        '<i class="fas fa-check text-success"></i>';
                }
            }
            
            const featureHtml = `
                <div class="feature-item">
                    <div class="feature-name">${label}</div>
                    <div class="feature-value">${displayValue} ${iconHtml}</div>
                </div>
            `;
            
            featuresGrid.innerHTML += featureHtml;
        }
        
        // Update timestamp
        timestamp.textContent = data.timestamp || new Date().toLocaleString();
        
        // Update JSON response for technical details
        jsonResponse.textContent = JSON.stringify(data, null, 2);
        
        // Show result container
        resultContainer.style.display = 'block';
    }

    // Show error function
    function showError(message) {
        resetUI();
        errorMessage.textContent = message;
        errorContainer.style.display = 'flex';
    }

    // Reset UI function
    function resetUI() {
        loader.style.display = 'none';
        resultContainer.style.display = 'none';
        errorContainer.style.display = 'none';
        technicalDetails.style.display = 'none';
        
        // Reset details toggle button
        const toggleText = detailsToggle.querySelector('span');
        const toggleIcon = detailsToggle.querySelector('i');
        toggleText.textContent = 'Show Technical Details';
        toggleIcon.classList.remove('fa-chevron-up');
        toggleIcon.classList.add('fa-chevron-down');
    }
    
    // Initialize the UI
    resetUI();
    urlInput.focus();