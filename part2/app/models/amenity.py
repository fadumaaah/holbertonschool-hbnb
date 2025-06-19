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