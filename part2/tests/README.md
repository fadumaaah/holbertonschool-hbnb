FIX README

Known Issues & Fixes During Testing
1. Error: TypeError: __init__() missing 1 required positional argument: 'name'
Cause: Passing incomplete data to the Amenity constructor (missing name).

Fix: Add validation in create_amenity method to check required fields before creating objects.

```python
def create_amenity(self, amenity_data):
    if 'name' not in amenity_data or not amenity_data['name']:
        raise ValueError("Name is required")
    amenity = Amenity(**amenity_data)
```

2. Failure: Tests expecting empty list but got non-empty list
Cause: In-memory repository was not cleared between tests, so data persisted across tests.

Fix: Clear in-memory storage before each test in setUp().

```python
from app.services import facade

class TestAmenityEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.clear_storage()

    def clear_storage(self):
        facade.amenity_repo._storage.clear()
```

3. Failure: Updating amenity with empty name returned status 200 instead of 400
Cause: Missing validation during update to check for empty name.

Fix: Add validation in put method of the Amenity API to raise ValueError on invalid input.

```python
def put(self, amenity_id):
    amenity_data = api.payload
    if 'name' not in amenity_data or not amenity_data['name']:
        raise ValueError("Name cannot be empty")
    updated_amenity = facade.update_amenity(amenity_id, amenity_data)
```

. Failure: test_update_user_not_found returned 400 instead of 404
Cause: The @api.route('/<user_id>') class (UserResource) was incorrectly nested inside the UserList class, so the PUT and GET methods were never properly registered with Flask.

Fix: Move the UserResource class outside of UserList to correctly register /users/<user_id> routes.

```python

# Before (incorrect nesting)
@api.route('/')
class UserList(Resource):
    ...
    @api.route('/<user_id>')
    class UserResource(Resource):

# After (fixed)
@api.route('/<user_id>')
class UserResource(Resource):
    ...
```

2. Error: AttributeError due to incorrect method call lower*()
Cause: The .lower() method was written incorrectly in the email comparison logic, causing a runtime error during validation.

Fix: Use the correct .lower() syntax to perform case-insensitive comparisons.

```python
# Incorrect
if user.email.lower() == email.strip().lower*():

# Correct
if user.email.lower() == email.strip().lower():
```