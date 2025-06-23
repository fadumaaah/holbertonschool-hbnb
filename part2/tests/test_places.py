import unittest
import uuid

from app import create_app
from app.services import facade

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        facade.place_repo._storage.clear()
        facade.user_repo._storage.clear()  # Clear users repo too

        # Create a test user and get their id
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com"
        })
        self.assertEqual(user_resp.status_code, 201)
        self.owner_id = user_resp.get_json()['id']

    def test_create_place_success(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cottage",
            "price": 100,
            "owner_id": self.owner_id,
            "latitude": 45.0,
            "longitude": 90.0
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_empty_title(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": 100,
            "owner_id": self.owner_id,
            "latitude": 45.0,
            "longitude": 90.0
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Nice Place",
            "price": -50,
            "owner_id": self.owner_id,
            "latitude": 45.0,
            "longitude": 90.0
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_latitude_out_of_range(self):
        for lat in [-91, 91]:
            response = self.client.post('/api/v1/places/', json={
                "title": "Test Place",
                "price": 50,
                "owner_id": self.owner_id,
                "latitude": lat,
                "longitude": 0
            })
            self.assertEqual(response.status_code, 400)

    def test_create_place_longitude_out_of_range(self):
        for lon in [-181, 181]:
            response = self.client.post('/api/v1/places/', json={
                "title": "Test Place",
                "price": 50,
                "owner_id": self.owner_id,
                "latitude": 0,
                "longitude": lon
            })
            self.assertEqual(response.status_code, 400)

    def test_get_place_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/places/{fake_id}')
        self.assertEqual(response.status_code, 404)

    def test_update_place_success(self):
        create_resp = self.client.post('/api/v1/places/', json={
            "title": "Old Title",
            "price": 80,
            "owner_id": self.owner_id,
            "latitude": 10,
            "longitude": 10
        })
        place_id = create_resp.get_json()['id']
        update_resp = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "New Title",
            "price": 90,
            "owner_id": self.owner_id,
            "latitude": 20,
            "longitude": 20
        })
        self.assertEqual(update_resp.status_code, 200)

    def test_update_place_invalid_latitude(self):
        create_resp = self.client.post('/api/v1/places/', json={
            "title": "Some Place",
            "price": 50,
            "owner_id": self.owner_id,
            "latitude": 0,
            "longitude": 0
        })
        place_id = create_resp.get_json()['id']
        update_resp = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Place",
            "price": 60,
            "owner_id": self.owner_id,
            "latitude": 100,  # invalid latitude
            "longitude": 0
        })
        self.assertEqual(update_resp.status_code, 400)

    def test_update_place_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.put(f'/api/v1/places/{fake_id}', json={
            "title": "Ghost Place",
            "price": 70,
            "owner_id": self.owner_id,
            "latitude": 0,
            "longitude": 0
        })
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
