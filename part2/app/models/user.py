#!/usr/bin/python3
"""
User class
"""


import re
from app.models.base_model import BaseModel


class User(BaseModel):
    # remove =None for password once proper authentication is added
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        # Calls the parent class (BaseModel) constructor first, which sets up the id, created_at, and updated_at attributes
        super().__init__()

        # validating first name exists and is 50 characters or less
        if not first_name or len(first_name) > 50:
            raise ValueError("First namem is required to be less than 50 characters.")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required to be less than 50 characters")
        if not self._is_valid_email(email):
            raise ValueError("Invalid email.")
        if password and not password.strip():
            # Note: strip() removes spaces - not password.strip() means "password is only spaces"
            raise ValueError("Password cannot be empty.")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin

    def _is_valid_email(self, email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email)
        # [^@]+ - checking if email has one or more characters that are not @
        # @ - followed by @
        # [^@]+ - checks if there are one or more characters that are not @
        # . - literal dot
        # [^@]+ - checking if there are one or or more characters that are not @
        # ensures matching email format
