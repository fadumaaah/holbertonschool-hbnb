#!/usr/bin/python3
"""
Places class
"""


from app.models.base_model import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Title is required and must be less than 100 characters")
        if price < 0:
            raise ValueError("Price must be a positive number")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0")
        if not (-180 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0")
        if not owner:
            raise ValueError("Owner (User) is required")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        # List to store related reviews
        self.reviews = []
        # List to store related amenties
        self.amenities = []

    def add_review(self, review):
        """
        Add review to place
        """
        self.reviews.append(review)

    def add_amentiy(self, amenity):
        """
        Add an amenity to a place
        """
        self.amenities.append(amenity)