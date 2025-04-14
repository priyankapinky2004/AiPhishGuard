PhishGuard is a machine learning-powered web application that detects phishing URLs. Built with Python, scikit-learn, and Flask, it provides an intuitive interface to analyze URLs and determine whether they are legitimate or potential phishing attempts.
┌────────────────────────────────────────────────────────────┐
│                                                            │
│  🛡️ PhishGuard: URL Phishing Detection                     │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Enter a URL to check...                      Check   │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Analysis Results                                     │  │
│  │                                                      │  │
│  │ https://example.com                                  │  │
│  │                                                      │  │
│  │ ✅ URL is Safe                                       │  │
│  │ This URL appears to be legitimate and safe to visit  │  │
│  │                                                      │  │
│  │ Phishing Probability: 1.23%                          │  │
│  │ [▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪▪] │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                            │
└────────────────────────────────────────────────────────────┘
🔍 Problem Statement
Phishing attacks remain one of the most common and effective forms of cybercrime, with millions of attempts occurring daily. These attacks trick users into visiting fraudulent websites that mimic legitimate ones to steal sensitive information such as login credentials, financial details, and personal data.
PhishGuard addresses this challenge by:

Providing real-time detection of phishing URLs
Analyzing URL characteristics using machine learning
Offering a user-friendly interface to check URLs before visiting them
Explaining why a URL might be suspicious through feature analysis

🛠️ Tech Stack
Backend

Python 3.8+: Core programming language
scikit-learn: Machine learning library for the classification model
Flask: Web framework for the API
pandas/numpy: Data processing and numerical operations
tld/python-whois/requests: URL processing and feature extraction

Frontend

HTML5/CSS3: Structure and styling
JavaScript (ES6+): Client-side interactivity
Font Awesome: Icons
Google Fonts: Typography

📋 Features

URL Analysis: Check any URL for phishing characteristics
Machine Learning Model: Random Forest classifier trained on URL features
Real-time Detection: Instant feedback on URL safety
Feature Breakdown: Detailed analysis of URL characteristics
Responsive Design: Works on desktop and mobile devices
Educational Content: Information about phishing and online safety

🗂️ Project Structure
phishing_detection/
│
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── app.log                     # Application logs
├── requirements.txt            # Project dependencies
│
├── data/                       # Data directory
│   ├── raw/                    # Raw data files
│   │   └── phishing_dataset.csv  # Original URL dataset
│   └── processed/              # Processed data files
│       └── processed_data.csv  # Processed features
│
├── models/                     # Model directory
│   ├── train.py                # Model training script
│   ├── predict.py              # Prediction functions
│   ├── evaluate.py             # Model evaluation
│   └── saved/                  # Saved model files
│       ├── best_model.pkl      # Trained model
│       ├── scaler.pkl          # Feature scaler
│       └── model_info.csv      # Model performance metrics
│
├── src/                        # Source code
│   ├── feature_extraction/     # Feature extraction code
│   │   └── extractor.py        # URL feature extractor
│   └── utils/                  # Utility functions
│       └── helpers.py          # Helper functions
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css           # CSS styles
│   ├── js/
│   │   └── script.js           # JavaScript code
│   └── images/                 # Image assets
│
├── templates/                  # HTML templates
│   └── index.html              # Main page template
│
├── notebooks/                  # Jupyter notebooks
│   └── exploratory.ipynb       # Data exploration
│
└── tests/                      # Test directory
    ├── test_extractor.py       # Test feature extraction
    └── test_model.py           # Test model performance
🚀 Setup Instructions
Prerequisites

Python 3.8 or higher
pip (Python package manager)
Git

Installation

Clone the repository
bashgit clone https://github.com/yourusername/phishguard.git 
cd phishguard

Create and activate a virtual environment
bash# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate

Install dependencies
bashpip install -r requirements.txt

Create necessary directories
bashmkdir -p data/raw data/processed models/saved static/images

Train the model or download pre-trained model
bash# To train the model
python models/train.py

# To download pre-trained model (alternative)
# Instructions would go here if you provide pre-trained models

Run the application
bashpython app.py

Access the application
Open a web browser and navigate to:
http://localhost:5000


📊 Model Training and Evaluation
The phishing detection model is trained on a dataset of legitimate and phishing URLs. The training process:

Extracts features from URLs (length, special characters, suspicious words, etc.)
Preprocesses and scales the features
Trains multiple models (Random Forest, Logistic Regression)
Evaluates models using cross-validation
Selects the best model based on F1 score

To retrain the model with your own dataset:

Place your CSV file in data/raw/ directory
Ensure it has 'url' and 'is_phishing' columns
Run the training script:
bashpython models/train.py --data_path your_dataset.csv


📝 Usage Guide
Checking a URL

Enter the URL you want to check in the input field
Click the "Check URL" button or press Enter
Wait for the analysis to complete
Review the results:

Verdict (Safe/Phishing)
Phishing probability
Feature breakdown
Technical details (optional)



Sample Output
For a legitimate URL:
json{
  "url": "https://www.google.com",
  "result": "safe",
  "probability": 0.0123,
  "features": {
    "url_length": 22,
    "contains_ip": 0,
    "num_special_chars": 2,
    "num_subdomains": 1,
    "has_https": 1,
    "suspicious_words": 0,
    "domain_age": 0,
    "redirect_count": 0
  },
  "timestamp": "2025-04-14 10:30:45"
}
For a phishing URL:
json{
  "url": "http://paypa1.com/secure/login.html",
  "result": "phishing",
  "probability": 0.9456,
  "features": {
    "url_length": 34,
    "contains_ip": 0,
    "num_special_chars": 2,
    "num_subdomains": 1,
    "has_https": 0,
    "suspicious_words": 1,
    "domain_age": 0,
    "redirect_count": 0
  },
  "timestamp": "2025-04-14 10:31:23"
}
🌐 API Documentation
PhishGuard provides a simple REST API that can be integrated into other applications.
Check URL Endpoint
URL: /check-url
Method: POST
Request Body:
json{
  "url": "https://example.com"
}
Response:
json{
  "url": "https://example.com",
  "result": "safe",
  "probability": 0.0123,
  "features": {
    "url_length": 19,
    "contains_ip": 0,
    "num_special_chars": 2,
    "num_subdomains": 1,
    "has_https": 1,
    "suspicious_words": 0,
    "domain_age": 0,
    "redirect_count": 0
  },
  "timestamp": "2025-04-14 10:30:45"
}
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

Fork the repository
Create your feature branch (git checkout -b feature/amazing-feature)
Commit your changes (git commit -m 'Add some amazing feature')
Push to the branch (git push origin feature/amazing-feature)
Open a Pull Request

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
👏 Acknowledgements

scikit-learn team for the machine learning library
Flask team for the web framework
Everyone who has contributed to the project
