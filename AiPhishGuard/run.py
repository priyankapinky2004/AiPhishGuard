#!/usr/bin/env python
"""
Run script for the Phishing URL Detection Flask API
"""
import os
from flask import Flask
from app.api import app

if __name__ == '__main__':
    # Get port from environment variable, default to 5000
    port = int(os.environ.get('PORT', 5000))
    
    # Run the app
    app.run(debug=False, host='0.0.0.0', port=port)