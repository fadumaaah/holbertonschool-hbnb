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