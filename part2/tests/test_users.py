import unittest
import uuid

from app import create_app
from app.services import facade

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        facade.user_repo._storage.clear()

    def test_create_user_success(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_missing_fields(self):
        response = self.client.post('/api/v1/users/', json={})
        self.assertEqual(response.status_code, 400)

    def test_create_user_duplicate_email(self):
        self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Wonder",
            "email": "alice@example.com"
        })
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Builder",
            "email": "alice@example.com"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_user_not_found(self):
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user_success(self):
        create_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Sam",
            "last_name": "Spade",
            "email": "sam.spade@example.com"
        })
        user_id = create_resp.get_json()['id']
        update_resp = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Samuel",
            "last_name": "Spade",
            "email": "samuel.spade@example.com"
        })
        self.assertEqual(update_resp.status_code, 200)

    def test_update_user_duplicate_email(self):
        resp1 = self.client.post('/api/v1/users/', json={
            "first_name": "User1",
            "last_name": "Test",
            "email": "user1@example.com"
        })
        user1_id = resp1.get_json()['id']

        self.client.post('/api/v1/users/', json={
            "first_name": "User2",
            "last_name": "Test",
            "email": "user2@example.com"
        })

        update_resp = self.client.put(f'/api/v1/users/{user1_id}', json={
            "first_name": "User1",
            "last_name": "Test",
            "email": "user2@example.com"
        })
        self.assertEqual(update_resp.status_code, 400)

        

    def test_update_user_not_found(self):
        fake_id = str(uuid.uuid4())
        response = self.client.put('/api/v1/users/{fake_id}', json={
            "first_name": "Ghost",
            "last_name": "User",
            "email": "unique-ghost@example.com"
        })
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
