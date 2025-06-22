from app.persistence.repository import InMemoryRepository
from datetime import datetime    
from app.models.user import User
from app.models.place import Place
from app.models.review import Review

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

    def create_amenity(self, amenity_data):
       existing = self.get_amenity_by_name(amenity_data.get('name'))
       if existing:
           raise ValueError('Amenity already exists')
       # Create amenity instance from dict, add it to repo and return created amenity
       amenity = amenity(**amenity_data)
       self.amenity_repo.add(amenity)
       return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)
    
    ### Need to debug, it does not work for getting an amenity by name
    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute('name', name)
 
    def get_all_amenities(self):
        return self.amenity_repo.get_all()
    
    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
    
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity
    
    def create_place(self, place_data: dict):
        owner = self.get_user(place_data.get("owner_id"))
        if not owner:
            raise ValueError("owner_id does not correspond to an existing user")

        amenities = []
        for aid in place_data.get("amenity_ids", []):
            amenity = self.get_amenity(aid)
            if not amenity:
                raise ValueError(f"Amenity id '{aid}' does not exist")
            amenities.append(amenity)
            
        new_place = Place(
            title       = place_data["title"],
            description = place_data.get("description", ""),
            price       = place_data["price"],
            latitude    = place_data["latitude"],
            longitude   = place_data["longitude"],
            owner       = owner
        )
        new_place.amenities = amenities
        
    def get_place(self, place_id):
        return self.place_repo.get(place_id)
    
    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data: dict):
        """
        Partial update. Unknown keys are ignored.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if "owner_id" in data:
            owner = self.get_user(data["owner_id"])
            if not owner:
                raise ValueError("owner_id does not correspond to an existing user")
            place.owner = owner

        if "amenity_ids" in data:
            amenities = []
            for aid in data["amenity_ids"]:
                amenity = self.get_amenity(aid)
                if not amenity:
                    raise ValueError(f"Amenity id '{aid}' does not exist")
                amenities.append(amenity)
            place.amenities = amenities

        for field in ["title", "description", "price", "latitude", "longitude"]:
            if field in data:
                setattr(place, field, data[field])

        place.updated_at = datetime.utcnow()
        self.place_repo.update(place_id, place)
        return place
    
    # REVIEW FACADE

    def create_review(self, review_data: dict):
        """
        Expected review_data keys: text, user_id, place_id
        """
        user = self.get_user(review_data.get("user_id"))
        if not user:
            raise ValueError("Invalid user_id")

        place = self.get_place(review_data.get("place_id"))
        if not place:
            raise ValueError("Invalid place_id")

        review = Review(text=review_data["text"], user=user, place=place)
        self.review_repo.add(review)

        place.reviews.append(review)

        return review


    def get_review(self, review_id):
        return self.review_repo.get(review_id)


    def get_reviews_for_place(self, place_id):
        place = self.get_place(place_id)
        return place.reviews if place else None


    def update_review(self, review_id, data: dict):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if "text" in data:
            if not data["text"].strip():
                raise ValueError("Review text cannot be empty")
            review.text = data["text"].strip()

        review.updated_at = datetime.utcnow()
        self.review_repo.update(review_id, review)
        return review


    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if not review:
            return False

        review.place.reviews = [
            r for r in review.place.reviews if r.id != review_id
        ]
        self.review_repo.delete(review_id)
        return True
    
    def create_review(self, review_data: dict):
        """
        Expects: text, rating (1–5), user_id, place_id
        """
        user = self.get_user(review_data.get("user_id"))
        if not user:
            raise ValueError("Invalid user_id")

        place = self.get_place(review_data.get("place_id"))
        if not place:
            raise ValueError("Invalid place_id")

        rating = review_data.get("rating")
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5")

        text = review_data.get("text")
        if not text or not text.strip():
            raise ValueError("Review text cannot be empty")

        review = Review(text=text.strip(), rating=rating, user=user, place=place)
        self.review_repo.add(review)

        place.reviews.append(review)

        return review


    def update_review(self, review_id, data: dict):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if "text" in data:
            if not data["text"].strip():
                raise ValueError("Review text cannot be empty")
            review.text = data["text"].strip()

        if "rating" in data:
            if not isinstance(data["rating"], int) or not (1 <= data["rating"] <= 5):
                raise ValueError("Rating must be an integer between 1 and 5")
            review.rating = data["rating"]

        review.updated_at = datetime.utcnow()
        self.review_repo.update(review_id, review)
        return review