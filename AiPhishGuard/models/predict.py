import joblib
import pandas as pd
import numpy as np
import os
from urllib.parse import urlparse
import re
import ipaddress

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

def predict_url(url, model_path='models/saved/best_model.pkl', scaler_path='models/saved/scaler.pkl'):
    """
    Predict whether a URL is phishing or legitimate
    
    Args:
        url (str): The URL to classify
        model_path (str): Path to the saved model
        scaler_path (str): Path to the saved scaler
        
    Returns:
        tuple: (prediction (0 or 1), probability, feature_dict)
    """
    # Check if model and scaler exist
    if not os.path.exists(model_path) or not os.path.exists(scaler_path):
        raise FileNotFoundError(f"Model or scaler not found at {model_path} or {scaler_path}")
    
    # Load model and scaler
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
    
    # Extract features
    feature_dict = extract_features_from_url(url)
    
    # Convert to DataFrame to ensure correct feature order
    feature_df = pd.DataFrame([feature_dict])
    
    # Scale features
    scaled_features = scaler.transform(feature_df)
    
    # Make prediction
    prediction = model.predict(scaled_features)[0]
    
    # Get probability
    probability = model.predict_proba(scaled_features)[0][1]
    
    return prediction, probability, feature_dict

def batch_predict(urls, model_path='models/saved/best_model.pkl', scaler_path='models/saved/scaler.pkl'):
    """
    Make predictions for a batch of URLs
    
    Args:
        urls (list): List of URLs to classify
        model_path (str): Path to the saved model
        scaler_path (str): Path to the saved scaler
        
    Returns:
        DataFrame: Contains URLs, predictions, and probabilities
    """
    results = []
    
    for url in urls:
        prediction, probability, features = predict_url(url, model_path, scaler_path)
        
        result = {
            'url': url,
            'is_phishing': prediction,
            'phishing_probability': probability,
            **features
        }
        
        results.append(result)
    
    return pd.DataFrame(results)

def main():
    """
    Example usage
    """
    # Example URLs
    test_urls = [
        "https://www.google.com",
        "http://suspicious-bank-login.com/verify",
        "https://github.com/repository/issues",
        "http://paypa1.com/secure/login.html"
    ]
    
    print("====== Phishing URL Detection ======\n")
    
    try:
        # Load model info if available
        if os.path.exists('models/saved/model_info.csv'):
            model_info = pd.read_csv('models/saved/model_info.csv')
            print("Loaded model info:")
            print(f"Model type: {model_info['model_type'].values[0]}")
            print(f"Accuracy: {model_info['accuracy'].values[0]:.4f}")
            print(f"Precision: {model_info['precision'].values[0]:.4f}")
            print(f"Recall: {model_info['recall'].values[0]:.4f}")
            print(f"F1 Score: {model_info['f1'].values[0]:.4f}\n")
        
        # Predict for individual URLs
        print("Individual URL predictions:")
        for url in test_urls:
            prediction, probability, _ = predict_url(url)
            result = "Phishing" if prediction == 1 else "Legitimate"
            print(f"URL: {url}")
            print(f"Prediction: {result}")
            print(f"Phishing Probability: {probability:.4f}\n")
        
        # Batch prediction
        print("Batch prediction results:")
        results_df = batch_predict(test_urls)
        print(results_df[['url', 'is_phishing', 'phishing_probability']].to_string(index=False))
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()