import pandas as pd
import numpy as np
import re
from urllib.parse import urlparse
from tld import get_tld
import whois
import requests
from datetime import datetime
import ipaddress

def extract_features(url):
    """
    Extract features from a URL for phishing detection
    
    Returns a dictionary of features
    """
    features = {}
    
    # Basic URL properties
    features['url_length'] = len(url)
    features['domain'] = urlparse(url).netloc
    
    # Check for IP address
    try:
        ipaddress.ip_address(features['domain'])
        features['contains_ip'] = 1
    except:
        features['contains_ip'] = 0
    
    # Count special characters
    features['num_special_chars'] = len(re.findall(r'[^a-zA-Z0-9]', url))
    
    # Number of subdomains
    if features['domain']:
        features['num_subdomains'] = len(features['domain'].split('.')) - 1
    else:
        features['num_subdomains'] = 0
    
    # Check for HTTPS
    features['has_https'] = 1 if url.startswith('https') else 0
    
    # Check for suspicious words
    suspicious_words = ['secure', 'login', 'signin', 'bank', 'account', 
                        'verify', 'confirm', 'update', 'authenticate', 
                        'validation', 'wallet', 'alert', 'limited', 'security']
    
    features['suspicious_words'] = sum(1 for word in suspicious_words if word in url.lower())
    
    # Advanced features (may need additional libraries)
    
    # Try to get domain age (in years)
    try:
        w = whois.whois(features['domain'])
        if w.creation_date:
            if isinstance(w.creation_date, list):
                creation_date = w.creation_date[0]
            else:
                creation_date = w.creation_date
            features['domain_age'] = (datetime.now() - creation_date).days / 365
        else:
            features['domain_age'] = 0
    except:
        features['domain_age'] = 0
    
    # Check for redirects
    try:
        response = requests.get(url, timeout=3, allow_redirects=False)
        if 'Location' in response.headers:
            features['redirect_count'] = 1
        else:
            features['redirect_count'] = 0
    except:
        features['redirect_count'] = 0
    
    # Additional features you could implement:
    # - TLS/SSL certificate validity
    # - Favicon check
    # - URL shortening service detection
    # - HTML/JavaScript features
    # - Domain popularity/ranking
    
    return features

# Example usage
def main():
    # Single URL example
    url = "https://www.google.com"
    features = extract_features(url)
    print(f"Features for {url}:")
    for key, value in features.items():
        print(f"{key}: {value}")
    
    # Process a CSV file with URLs
    df = pd.read_csv('urls.csv')  # Assumes a CSV with a 'url' column
    
    # Create empty columns for features
    feature_columns = ['url_length', 'contains_ip', 'num_special_chars', 
                      'num_subdomains', 'has_https', 'suspicious_words',
                      'domain_age', 'redirect_count']
    
    for col in feature_columns:
        df[col] = np.nan
    
    # Extract features for each URL
    for i, row in df.iterrows():
        url = row['url']
        try:
            features = extract_features(url)
            for feature, value in features.items():
                if feature in feature_columns:
                    df.at[i, feature] = value
        except Exception as e:
            print(f"Error processing {url}: {e}")
    
    # Save the processed data
    df.to_csv('urls_with_features.csv', index=False)
    print("Features extracted and saved to 'urls_with_features.csv'")

if __name__ == "__main__":
    main()