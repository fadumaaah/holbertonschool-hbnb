from app.persistence.repository import InMemoryRepository
from app.models.amenity import Amenity


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        # Logic will be implemented in later tasks
        pass

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass

    def create_amenity(self, amenity_data):
       existing = self.get_amenity_by_name(amenity_data.get('name'))
       if existing:
           raise ValueError('Amenity already exists')
       # Create amenity instance from dict, add it to repo and return created amenity
       amenity = Amenity(**amenity_data)
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


    
    