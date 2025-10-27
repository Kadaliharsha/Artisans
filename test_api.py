"""
Test the ArtisanHub API
"""
import requests # type: ignore
import json

# Base URL
BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoints"""
    print("🔸 Testing health endpoints...")
    
    # Test root endpoint
    response = requests.get(f"{BASE_URL}/")
    print(f"  Root endpoint: {response.status_code}")
    
    # Test health endpoint
    response = requests.get(f"{BASE_URL}/health")
    print(f"  Health endpoint: {response.status_code}")
    
    return response.status_code == 200

def test_users():
    """Test user endpoints"""
    print("🔸 Testing user endpoints...")
    
    # Test create user
    print("  Creating user...")
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "role": "customer"
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/users", json=user_data)
    print(f"  Create user: {response.status_code}")
    
    if response.status_code == 201:
        user = response.json()
        print(f"  Created user with ID: {user['id']}")
        
        # Test get user by ID
        user_id = user['id']
        response = requests.get(f"{BASE_URL}/api/v1/users/{user_id}")
        print(f"  Get user by ID: {response.status_code}")
        
        # Test get all users
        response = requests.get(f"{BASE_URL}/api/v1/users")
        print(f"  Get all users: {response.status_code}")
        
        # Test debug endpoint
        response = requests.get(f"{BASE_URL}/api/v1/users/debug")
        print(f"  Debug endpoint: {response.status_code}")
        
        return response.status_code == 200
    
    return False

if __name__ == "__main__":
    print("🚀 Starting API tests...")
    
    # Start uvicorn server in another terminal:
    # uvicorn main:app --reload
    
    success = True
    
    # Run tests
    if not test_health():
        success = False
        
    if not test_users():
        success = False
    
    print(f"\n🎯 Test results: {'SUCCESS' if success else 'FAILED'}")