import unittest
import uuid

from app import create_app
from app.services import facade

class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        facade.review_repo._storage.clear()
        facade.user_repo._storage.clear()
        facade.place_repo._storage.clear()

        # Create a user for owner of reviews
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "reviewer@example.com"
        })
        self.assertEqual(user_resp.status_code, 201)
        self.user_id = user_resp.get_json()['id']

        # Create a place to be reviewed
        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Review Place",
            "price": 50,
            "owner_id": self.user_id,
            "latitude": 10,
            "longitude": 10
        })
        self.assertEqual(place_resp.status_code, 201)
        self.place_id = place_resp.get_json()['id']

    def test_create_review_success(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "This place was amazing!",
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": 5
            
        })
        self.assertEqual(response.status_code, 201)

    def test_create_review_empty_text(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_user_id(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "rating": 5,
            # Missing user_id
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_place_id(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "rating": 5,
            "user_id": self.user_id
            # Missing place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user_id(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "rating": 5,
            "user_id": str(uuid.uuid4()),  # non-existent user
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 404)

    def test_create_review_invalid_place_id(self):
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Nice place",
            "user_id": self.user_id,
            "rating": 5,
            "place_id": str(uuid.uuid4())  # non-existent place
        })
        self.assertEqual(response.status_code, 404)

    def test_get_review_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.get(f'/api/v1/reviews/{fake_id}')
        self.assertEqual(response.status_code, 404)

    def test_update_review_success(self):
        create_resp = self.client.post('/api/v1/reviews/', json={
            "text": "Old review text",
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_resp.get_json()['id']
        update_resp = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated review text",
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(update_resp.status_code, 200)

    def test_update_review_empty_text(self):
        create_resp = self.client.post('/api/v1/reviews/', json={
            "text": "Valid review text",
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_resp.get_json()['id']
        update_resp = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "",
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(update_resp.status_code, 400)

    def test_update_review_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.put(f'/api/v1/reviews/{fake_id}', json={
            "text": "Ghost review",
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 404)

    def test_delete_review_success(self):
        create_resp = self.client.post('/api/v1/reviews/', json={
            "text": "Review to delete",
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_resp.get_json()['id']
        delete_resp = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(delete_resp.status_code, 200)
        # Verify it's really deleted
        get_resp = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_resp.status_code, 404)

if __name__ == '__main__':
    unittest.main()
