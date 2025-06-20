from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # USER FACADE
    # takes a dictionary of user data
    def create_user(self, user_data):
        # using dictionary unpacking (**)
        user = User(**user_data)
        self.user_repo.add(user)
        return (user)

    # takes user id and returns the user object (or None if not found)
    def get_user(self, user_id):
        return (self.user_repo.get(user_id))

    def update_user(self, user_id, data):
        # checks if user exists
        user = self.get_user(user_id)
        # if user doesn't exist, returns None to indicate failure
        if not user:
            return (None)
        # if user exists, calls repo to update with new data
        self.user_repo.update(user_id, data)
        # fetches and returns the updated user (to ensure we have the latest data with updated timestamps)
        return (self.user_repo.get(user_id))

    def get_user_by_email(self, email):
        """Get user by email (case-insensitive)"""
        # checks if email exists
        if not email or not email.strip():
            return (None)

        # search through all users manually
        all_users = self.user_repo.get_all()
        for user in all_users:
            # email strip lower - removes spaces and converts to lowercase
            # user email lower - converts stored email to lowercase
            # compares them for equality
            if user.email.lower() == email.strip().lower*():
                return (user)
        # returns matching user or none
        return (None)

    # returns list of all users
    def get_all_users(self):
        return (self.user_repo.get_all())

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass