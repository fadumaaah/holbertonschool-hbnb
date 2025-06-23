import unittest
import uuid

from app import create_app
from app.services import facade

class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        facade.place_repo._storage.clear()

    def test_create_place_success(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Cottage",
            "price": 100,
            "latitude": 45.0,
            "longitude": 90.0
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_empty_title(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": 100,
            "latitude": 45.0,
            "longitude": 90.0
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_negative_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Nice Place",
            "price": -50,
            "latitude": 45.0,
            "longitude": 90.0
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_latitude_out_of_range(self):
        for lat in [-91, 91]:
            response = self.client.post('/api/v1/places/', json={
                "title": "Test Place",
                "price": 50,
                "latitude": lat,
                "longitude": 0
            })
            self.assertEqual(response.status_code, 400)

    def test_create_place_longitude_out_of_range(self):
        for lon in [-181, 181]:
            response = self.client.post('/api/v1/places/', json={
                "title": "Test Place",
                "price": 50,
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
            "latitude": 10,
            "longitude": 10
        })
        place_id = create_resp.get_json()['id']
        update_resp = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "New Title",
            "price": 90,
            "latitude": 20,
            "longitude": 20
        })
        self.assertEqual(update_resp.status_code, 200)

    def test_update_place_invalid_latitude(self):
        create_resp = self.client.post('/api/v1/places/', json={
            "title": "Some Place",
            "price": 50,
            "latitude": 0,
            "longitude": 0
        })
        place_id = create_resp.get_json()['id']
        update_resp = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Place",
            "price": 60,
            "latitude": 100,  # invalid latitude
            "longitude": 0
        })
        self.assertEqual(update_resp.status_code, 400)

    def test_update_place_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.put(f'/api/v1/places/{fake_id}', json={
            "title": "Ghost Place",
            "price": 70,
            "latitude": 0,
            "longitude": 0
        })
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
