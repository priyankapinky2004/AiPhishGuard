from flask import Flask, request, jsonify, render_template
import joblib
import os
import numpy as np
import pandas as pd
from urllib.parse import urlparse
import re
import ipaddress
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Create Flask app
app = Flask(__name__)

# Define paths to model and scaler
MODEL_PATH = 'models/saved/best_model.pkl'
SCALER_PATH = 'models/saved/scaler.pkl'

# Load model and scaler at startup
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    logging.info("Model and scaler loaded successfully")
except Exception as e:
    logging.error(f"Error loading model or scaler: {str(e)}")
    model = None
    scaler = None

def extract_features_from_url(url):
    """
    Extract features from a single URL
    
    Args:
        url (str): The URL to extract features from
        
    Returns:
        dict: Dictionary containing features
    """
    features = {}
    
    # Basic URL properties
    features['url_length'] = len(url)
    
    # Get domain
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    
    # Check for IP address
    try:
        ipaddress.ip_address(domain)
        features['contains_ip'] = 1
    except:
        features['contains_ip'] = 0
    
    # Count special characters
    features['num_special_chars'] = len(re.findall(r'[^a-zA-Z0-9]', url))
    
    # Number of subdomains
    if domain:
        features['num_subdomains'] = len(domain.split('.')) - 1
    else:
        features['num_subdomains'] = 0
    
    # Check for HTTPS
    features['has_https'] = 1 if url.startswith('https') else 0
    
    # Check for suspicious words
    suspicious_words = ['secure', 'login', 'signin', 'bank', 'account', 
                        'verify', 'confirm', 'update', 'authenticate', 
                        'validation', 'wallet', 'alert', 'limited', 'security']
    
    features['suspicious_words'] = sum(1 for word in suspicious_words if word in url.lower())
    
    # Use placeholder values for features that require external API calls
    features['domain_age'] = 0  # This would require whois lookup
    features['redirect_count'] = 0  # This would require making an HTTP request
    
    return features

def make_prediction(url):
    """
    Make a prediction for a given URL
    
    Args:
        url (str): URL to check
        
    Returns:
        dict: Prediction results
    """
    try:
        # Extract features
        features = extract_features_from_url(url)
        
        # Convert to DataFrame
        feature_df = pd.DataFrame([features])
        
        # Scale features
        scaled_features = scaler.transform(feature_df)
        
        # Make prediction
        prediction = int(model.predict(scaled_features)[0])
        
        # Get probability
        probability = float(model.predict_proba(scaled_features)[0][1])
        
        # Determine result
        result = "phishing" if prediction == 1 else "safe"
        
        # Create response
        response = {
            "url": url,
            "result": result,
            "probability": round(probability, 4),
            "features": features,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Log prediction
        logging.info(f"Prediction for {url}: {result} (probability: {probability:.4f})")
        
        return response
    
    except Exception as e:
        logging.error(f"Error making prediction for {url}: {str(e)}")
        raise

@app.route('/')
def index():
    """
    Render the main page
    """
    return render_template('index.html')

@app.route('/check-url', methods=['POST'])
def check_url():
    """
    API endpoint to check if a URL is phishing or safe
    
    Expected JSON input:
    {
        "url": "https://example.com"
    }
    """
    # Check if model is loaded
    if model is None or scaler is None:
        return jsonify({
            "error": "Model not loaded. Please check server logs."
        }), 500
    
    # Get JSON data
    data = request.get_json()
    
    # Validate input
    if not data or 'url' not in data:
        return jsonify({
            "error": "Missing 'url' parameter in request"
        }), 400
    
    url = data['url']
    
    # Validate URL
    if not url or not isinstance(url, str):
        return jsonify({
            "error": "Invalid URL provided"
        }), 400
    
    try:
        # Make prediction
        result = make_prediction(url)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            "error": f"Error processing URL: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    """
    status = "ok" if model is not None and scaler is not None else "error"
    return jsonify({
        "status": status,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)