import requests
import json

# Using Flask's test client instead of running a real server
from config import app, db
from models import Episode, Guest, Appearance
from routes import *  # Import routes to register them with the app
import os

# Create a test client
client = app.test_client()

def test_get_episodes():
    print("Testing GET /episodes...")
    with app.app_context():
        response = client.get('/episodes')
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.data}")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        if data:
            assert 'id' in data[0]
            assert 'date' in data[0]
            assert 'number' in data[0]
            assert 'appearances' not in data[0]
        print("✅ GET /episodes passed")

def test_get_episode_by_id():
    print("Testing GET /episodes/1...")
    with app.app_context():
        response = client.get('/episodes/1')
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.data}")
        assert response.status_code == 200
        data = response.get_json()
        assert data['id'] == 1
        assert 'appearances' in data
        assert isinstance(data['appearances'], list)
        if data['appearances']:
            assert 'guest' in data['appearances'][0]
            assert 'name' in data['appearances'][0]['guest']
        print("✅ GET /episodes/:id passed")

def test_get_episode_not_found():
    print("Testing GET /episodes/999 (Not Found)...")
    with app.app_context():
        response = client.get('/episodes/999')
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.data}")
        assert response.status_code == 404
        assert response.get_json() == {"error": "Episode not found"}
        print("✅ GET /episodes/:id (not found) passed")

def test_get_guests():
    print("Testing GET /guests...")
    with app.app_context():
        response = client.get('/guests')
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.data}")
        assert response.status_code == 200
        data = response.get_json()
        assert isinstance(data, list)
        if data:
            assert 'id' in data[0]
            assert 'name' in data[0]
            assert 'occupation' in data[0]
        print("✅ GET /guests passed")

def test_post_appearance_success():
    print("Testing POST /appearances (Success)...")
    with app.app_context():
        payload = {
            "rating": 5,
            "episode_id": 2,
            "guest_id": 3
        }
        response = client.post('/appearances', json=payload)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.data}")
        assert response.status_code == 201
        data = response.get_json()
        assert data['rating'] == 5
        assert data['episode_id'] == 2
        assert data['guest_id'] == 3
        assert 'episode' in data
        assert 'guest' in data
        print("✅ POST /appearances (success) passed")

def test_post_appearance_invalid_rating():
    print("Testing POST /appearances (Invalid Rating)...")
    with app.app_context():
        payload = {
            "rating": 6,
            "episode_id": 1,
            "guest_id": 1
        }
        response = client.post('/appearances', json=payload)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.data}")
        assert response.status_code == 400
        assert "errors" in response.get_json()
        print("✅ POST /appearances (invalid rating) passed")

if __name__ == "__main__":
    try:
        test_get_episodes()
        test_get_episode_by_id()
        test_get_episode_not_found()
        test_get_guests()
        test_post_appearance_success()
        test_post_appearance_invalid_rating()
        print("\nAll tests passed successfully!")
    except AssertionError as e:
        print(f"\n❌ Test failed!")
        import traceback
        traceback.print_exc()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()

