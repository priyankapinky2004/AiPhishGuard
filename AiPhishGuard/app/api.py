import requests
import json

# API endpoint
API_URL = "http://localhost:5000/check-url"

# Test URLs
test_urls = [
    "https://www.google.com",
    "http://suspicious-bank-login.com/verify",
    "https://github.com/repository/issues",
    "http://paypa1.com/secure/login.html",
    "https://www.amazon.com/dp/B07FZ8S74R/"
]

def test_api():
    """
    Test the phishing detection API with several URLs
    """
    print("Testing Phishing URL Detection API\n")
    
    # Check each URL
    for url in test_urls:
        print(f"Checking URL: {url}")
        
        # Prepare request data
        payload = {"url": url}
        headers = {"Content-Type": "application/json"}
        
        try:
            # Send POST request to API
            response = requests.post(API_URL, data=json.dumps(payload), headers=headers)
            
            # Check response status
            if response.status_code == 200:
                # Parse JSON response
                result = response.json()
                
                # Print result
                print(f"Result: {result['result']}")
                print(f"Probability: {result['probability']:.4f}")
                print(f"Features: {json.dumps(result['features'], indent=2)}")
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
        
        except Exception as e:
            print(f"Exception: {str(e)}")
        
        print("-" * 50)

# Using curl command (for documentation)
curl_commands = """
# Test with a legitimate URL
curl -X POST http://localhost:5000/check-url \\
  -H "Content-Type: application/json" \\
  -d '{"url": "https://www.google.com"}'

# Test with a suspicious URL
curl -X POST http://localhost:5000/check-url \\
  -H "Content-Type: application/json" \\
  -d '{"url": "http://paypa1.com/secure/login.html"}'

# Health check endpoint
curl -X GET http://localhost:5000/health
"""

if __name__ == "__main__":
    print("Starting API tests...\n")
    test_api()
    
    print("\nCURL commands for manual testing:")
    print(curl_commands)