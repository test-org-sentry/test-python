#!/usr/bin/env python3
"""
Main entry point for the Sentry test application.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from app.app import app
from app.api_endpoints import api_bp

# Register API blueprint
app.register_blueprint(api_bp)

if __name__ == '__main__':
    print("Starting Sentry Test Application...")
    print("Visit http://localhost:5000 to access the test interface")
    print("API endpoints available at http://localhost:5000/api/v1/")
    app.run(debug=True, host='0.0.0.0', port=5000)
