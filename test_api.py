
import requests
import json

BASE_URL = "http://127.0.0.1:5005"

def test_get_episodes():
    print("Testing GET /episodes...")
    response = requests.get(f"{BASE_URL}/episodes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert 'id' in data[0]
        assert 'date' in data[0]
        assert 'number' in data[0]
        assert 'appearances' not in data[0]
    print("✅ GET /episodes passed")

def test_get_episode_by_id():
    print("Testing GET /episodes/1...")
    response = requests.get(f"{BASE_URL}/episodes/1")
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 1
    assert 'appearances' in data
    assert isinstance(data['appearances'], list)
    if data['appearances']:
        assert 'guest' in data['appearances'][0]
        assert 'name' in data['appearances'][0]['guest']
    print("✅ GET /episodes/:id passed")

def test_get_episode_not_found():
    print("Testing GET /episodes/999 (Not Found)...")
    response = requests.get(f"{BASE_URL}/episodes/999")
    assert response.status_code == 404
    assert response.json() == {"error": "Episode not found"}
    print("✅ GET /episodes/:id (not found) passed")

def test_get_guests():
    print("Testing GET /guests...")
    response = requests.get(f"{BASE_URL}/guests")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    if data:
        assert 'id' in data[0]
        assert 'name' in data[0]
        assert 'occupation' in data[0]
    print("✅ GET /guests passed")

def test_post_appearance_success():
    print("Testing POST /appearances (Success)...")
    payload = {
        "rating": 5,
        "episode_id": 2,
        "guest_id": 3
    }
    response = requests.post(f"{BASE_URL}/appearances", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data['rating'] == 5
    assert data['episode_id'] == 2
    assert data['guest_id'] == 3
    assert 'episode' in data
    assert 'guest' in data
    print("✅ POST /appearances (success) passed")

def test_post_appearance_invalid_rating():
    print("Testing POST /appearances (Invalid Rating)...")
    payload = {
        "rating": 6,
        "episode_id": 1,
        "guest_id": 1
    }
    response = requests.post(f"{BASE_URL}/appearances", json=payload)
    assert response.status_code == 400
    assert "errors" in response.json()
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
