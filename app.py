"""
Simple Flask Web Application
A demonstration Flask app for Jenkins CI/CD pipeline.
"""

from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    """Home page route."""
    return "Welcome to the Flask Application! CI/CD Pipeline Demo."


@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({
        "status": "healthy",
        "message": "Application is running"
    })


@app.route('/api/data')
def get_data():
    """Sample API endpoint returning JSON data."""
    return jsonify({
        "items": [
            {"id": 1, "name": "Item 1", "description": "First item"},
            {"id": 2, "name": "Item 2", "description": "Second item"},
            {"id": 3, "name": "Item 3", "description": "Third item"}
        ],
        "total": 3
    })


@app.route('/api/status')
def get_status():
    """Application status endpoint."""
    return jsonify({
        "app_name": "Flask CI/CD Demo",
        "version": "1.0.0",
        "environment": "development"
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
