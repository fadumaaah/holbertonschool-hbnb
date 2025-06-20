#!/usr/bin/python3
"""
Amenity class
"""


from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, description=""):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError("Amenity name is required to be less than 50 characters")

        self.name = name
        self.description = description

    # update ammenity attributes from a dict
    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)