#!/usr/bin/python3
"""
Base model class for common attributes
"""


# unique identifiers model
import uuid
# imports datetime class from datetime module to work with dates/times
from datetime import datetime


class BaseModel:
    def __init__(self):
        # 4 is the version of UUID being generated
        # 4 completely randomises numbers
        # creates a new id for each object instance
        self.id = str(uuid.uuid4())
        # sets created_at attribute to current date and time when the object is created
        self.created_at = datetime.now()
        # Sets the updated_at attribute to the current date and time (initially same as created_at)
        self.updated_at = datetime.now()

    def save(self):
        """
        Update the updated_at timestamp whenever the object is modified
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update the attributes of the object based on the provided dictionary
        """
        # loops through each key-value pair in data dictionary
        for key, value in data.items():
            # checks if the object has an attribute with that key name (safety check)
            if hasattr(self, key):
                # sets the attribute to new value if it exists
                setattr(self, key, value)
                # updates the updated_at timestamp
                self.save()

    def delete(self):
        """
        Placeholder for deleting this object later
        """
        pass