from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    """Render the main page"""
    return "<h1>PhishGuard</h1><p>Phishing URL Detection System</p>"

@app.route('/check-url', methods=['POST'])
def check_url():
    """Simple mock version of the URL checker"""
    data = request.get_json()
    
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL parameter"}), 400
    
    url = data['url']
    
    # Simple mock response
    return jsonify({
        "url": url,
        "result": "safe" if "google" in url.lower() else "phishing",
        "probability": 0.1 if "google" in url.lower() else 0.9,
        "features": {
            "url_length": len(url),
            "contains_ip": 0,
            "num_special_chars": url.count('.'),
            "num_subdomains": url.count('.') - 1 if url.count('.') > 0 else 0,
            "has_https": 1 if url.startswith("https") else 0,
            "suspicious_words": 0,
            "domain_age": 0,
            "redirect_count": 0
        }
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(debug=True, host='127.0.0.1', port=5000)