import unittest
from app import create_app
from app.services import facade

class TestAmenityEndpoints(unittest.TestCase):


    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.clear_storage() 

    ## To clear storage if needed for tests
    def clear_storage(self):
        facade.amenity_repo._storage.clear()


    def test_create_amenity(self):
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Pool"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_amenity_missing_name(self):
        response = self.client.post('/api/v1/amenities/', json={})
        self.assertEqual(response.status_code, 400)

    def test_create_amenity_empty_name(self):
        response = self.client.post('/api/v1/amenities/', json={"name": ""})
        self.assertEqual(response.status_code, 400)

    def test_get_amenity_not_found(self):
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_get_all_amenities_empty(self):
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_update_amenity(self):
        # create first
        create_resp = self.client.post('/api/v1/amenities/', json={"name": "Gym"})
        amenity_id = create_resp.get_json()['id']

        # update
        update_resp = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Fitness Center"})
        self.assertEqual(update_resp.status_code, 200)

    def test_update_amenity_empty_name(self):
        create_resp = self.client.post('/api/v1/amenities/', json={"name": "Sauna"})
        amenity_id = create_resp.get_json()['id']

        update_resp = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": ""})
        self.assertEqual(update_resp.status_code, 400)
