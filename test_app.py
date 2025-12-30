"""
Unit Tests for Flask Application
Tests all routes and endpoints using pytest.
"""

import pytest
from app import app


@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


class TestHomeRoute:
    """Tests for the home route."""
    
    def test_home_status_code(self, client):
        """Test that home route returns 200 status code."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_home_content(self, client):
        """Test that home route returns expected content."""
        response = client.get('/')
        assert b'Welcome to the Flask Application' in response.data


class TestHealthRoute:
    """Tests for the health check route."""
    
    def test_health_status_code(self, client):
        """Test that health route returns 200 status code."""
        response = client.get('/health')
        assert response.status_code == 200
    
    def test_health_json_response(self, client):
        """Test that health route returns valid JSON."""
        response = client.get('/health')
        json_data = response.get_json()
        assert json_data['status'] == 'healthy'
        assert 'message' in json_data


class TestAPIDataRoute:
    """Tests for the API data route."""
    
    def test_api_data_status_code(self, client):
        """Test that API data route returns 200 status code."""
        response = client.get('/api/data')
        assert response.status_code == 200
    
    def test_api_data_json_structure(self, client):
        """Test that API data route returns correct JSON structure."""
        response = client.get('/api/data')
        json_data = response.get_json()
        assert 'items' in json_data
        assert 'total' in json_data
        assert json_data['total'] == 3
    
    def test_api_data_items_content(self, client):
        """Test that API data returns expected items."""
        response = client.get('/api/data')
        json_data = response.get_json()
        assert len(json_data['items']) == 3
        assert json_data['items'][0]['id'] == 1


class TestAPIStatusRoute:
    """Tests for the API status route."""
    
    def test_api_status_code(self, client):
        """Test that API status route returns 200 status code."""
        response = client.get('/api/status')
        assert response.status_code == 200
    
    def test_api_status_content(self, client):
        """Test that API status returns expected content."""
        response = client.get('/api/status')
        json_data = response.get_json()
        assert json_data['app_name'] == 'Flask CI/CD Demo'
        assert json_data['version'] == '1.0.0'


class TestInvalidRoutes:
    """Tests for invalid routes."""
    
    def test_404_for_invalid_route(self, client):
        """Test that invalid routes return 404."""
        response = client.get('/invalid-route')
        assert response.status_code == 404


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
