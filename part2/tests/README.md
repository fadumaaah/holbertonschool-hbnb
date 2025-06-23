# Testing Process Documentation

## 1. Test Environment  
- OS: macOS 
- Python Version: 3.9.6 
- Flask Version: 3.1.1 
- Database / Storage: In-memory repositories (no external DB)  
- Other: Unit tests run with `unittest` module, using Flask test client

## 2. Tools and Frameworks Used  
- Python `unittest`  
- Flask test client (`self.app.test_client()`)  
- No external database; uses in-memory storage cleared between tests

## 3. Endpoints Tested  

| Endpoint                      | HTTP Method       | Description                               |
|-------------------------------|-------------------|-----------------------------------------|
| `/api/v1/users/`              | POST              | Create new user                         |
| `/api/v1/users/{user_id}`     | GET, PUT          | Retrieve or update user by ID           |
| `/api/v1/places/`             | POST              | Create new place                        |
| `/api/v1/places/{place_id}`   | GET, PUT          | Retrieve or update place by ID           |
| `/api/v1/reviews/`            | POST              | Create new review                      |
| `/api/v1/reviews/{review_id}` | GET, PUT, DELETE  | Retrieve, update, or delete review by ID |
| `/api/v1/amenities/`          | POST              | Create new amenity                     |
| `/api/v1/amenities/{amenity_id}` | GET, PUT      | Retrieve or update amenity by ID         |

## 4. Input Data Used  

These are example payloads used in the unit tests. `self.user_id` and `self.place_id` are dynamically created in test setup and referenced in dependent tests.

### User (Valid Creation)
```json
{
  "first_name": "Jane",
  "last_name": "Doe",
  "email": "jane.doe@example.com"
}
```

### Amenity (Valid Creation)
```json
{
  "name": "Wi-Fi"
}
```

### Place (Valid Creation)
```json
{
  "title": "Cozy Cabin",
  "price": 120,
  "owner_id": self.user_id,
  "latitude": 45.0,
  "longitude": -75.0
}
```

### Review (Valid Creation)
```json
{
  "text": "Great stay!",
  "user_id": self.user_id,
  "place_id": self.place_id,
  "rating": 5
}
```

> ⚙️ Note: `self.user_id` and `self.place_id` represent IDs created during test setup.

## 5. Expected Output vs. Actual Output

### Users

1. **Create user with valid data**  
   - *Description:* Creating a user with all required fields (`first_name`, `last_name`, `email`).  
   - Expected: `201 Created` with new user data returned.  
   - Actual: `201 Created` — user created successfully.  
   - Status: Pass

2. **Create user missing fields**  
   - *Description:* Attempt to create a user with no data provided.  
   - Expected: `400 Bad Request` due to validation failure.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

3. **Create user duplicate email**  
   - *Description:* Creating a second user with an email that already exists in storage.  
   - Expected: `400 Bad Request` to prevent duplicates.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

4. **Get user not found**  
   - *Description:* Requesting a user by a non-existent user ID.  
   - Expected: `404 Not Found`.  
   - Actual: `404 Not Found`.  
   - Status: Pass

5. **Update user success**  
   - *Description:* Update an existing user’s information with valid data.  
   - Expected: `200 OK` and updated user data returned.  
   - Actual: `200 OK`.  
   - Status: Pass

6. **Update user duplicate email**  
   - *Description:* Attempt to update a user’s email to one already assigned to another user.  
   - Expected: `400 Bad Request` to avoid duplicate emails.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

7. **Update user not found**  
   - *Description:* Attempt to update a user with an ID that does not exist.  
   - Expected: `404 Not Found`.  
   - Actual: `404 Not Found`.  
   - Status: Pass

### Amenities

1. **Create amenity with valid data**  
   - *Description:* Creating an amenity with a valid name.  
   - Expected: `201 Created` with new amenity data.  
   - Actual: `201 Created` — amenity created successfully.  
   - Status: Pass

2. **Create amenity missing name**  
   - *Description:* Attempt to create an amenity without a name field.  
   - Expected: `400 Bad Request` due to missing required data.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

3. **Create amenity empty name**  
   - *Description:* Attempt to create an amenity with an empty string as name.  
   - Expected: `400 Bad Request` due to invalid input.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

4. **Get amenity not found**  
   - *Description:* Retrieve amenity by a non-existent ID.  
   - Expected: `404 Not Found`.  
   - Actual: `404 Not Found`.  
   - Status: Pass

5. **Get all amenities when none exist**  
   - *Description:* Retrieve list of all amenities when storage is empty.  
   - Expected: `200 OK` with empty list.  
   - Actual: `200 OK` with empty list.  
   - Status: Pass

6. **Update amenity success**  
   - *Description:* Update existing amenity’s name with valid data.  
   - Expected: `200 OK` and updated amenity data.  
   - Actual: `200 OK`.  
   - Status: Pass

7. **Update amenity with empty name**  
   - *Description:* Attempt to update amenity’s name to an empty string.  
   - Expected: `400 Bad Request` due to invalid input.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

### Places

1. **Create place with valid data**  
   - *Description:* Create a place with all required valid fields (`title`, `price`, `owner_id`, `latitude`, `longitude`).  
   - Expected: `201 Created` with new place data.  
   - Actual: `201 Created`.  
   - Status: Pass

2. **Create place with empty title**  
   - *Description:* Attempt to create a place with an empty string as the title.  
   - Expected: `400 Bad Request` due to invalid input.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

3. **Create place with negative price**  
   - *Description:* Attempt to create a place with a negative price value.  
   - Expected: `400 Bad Request` due to invalid input.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

4. **Create place with latitude out of range**  
   - *Description:* Attempt to create a place with latitude less than -90 or greater than 90.  
   - Expected: `400 Bad Request`.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

5. **Create place with longitude out of range**  
   - *Description:* Attempt to create a place with longitude less than -180 or greater than 180.  
   - Expected: `400 Bad Request`.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

6. **Get place not found**  
   - *Description:* Retrieve a place by a non-existent ID.  
   - Expected: `404 Not Found`.  
   - Actual: `404 Not Found`.  
   - Status: Pass

7. **Update place success**  
   - *Description:* Update an existing place with valid data.  
   - Expected: `200 OK` and updated place data.  
   - Actual: `200 OK`.  
   - Status: Pass

8. **Update place with invalid latitude**  
   - *Description:* Attempt to update a place’s latitude to an invalid value (outside -90 to 90).  
   - Expected: `400 Bad Request`.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

9. **Update place not found**  
   - *Description:* Attempt to update a place by a non-existent ID.  
   - Expected: `404 Not Found`.  
   - Actual: `404 Not Found`.  
   - Status: Pass

### Reviews

1. **Create review with valid data**  
   - *Description:* Create a review with valid `text`, `user_id`, `place_id`, and `rating`.  
   - Expected: `201 Created` with new review data.  
   - Actual: `201 Created`.  
   - Status: Pass

2. **Create review with empty text**  
   - *Description:* Attempt to create a review with empty text.  
   - Expected: `400 Bad Request`.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

3. **Create review missing user_id**  
   - *Description:* Attempt to create a review without specifying `user_id`.  
   - Expected: `400 Bad Request`.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

4. **Create review missing place_id**  
   - *Description:* Attempt to create a review without specifying `place_id`.  
   - Expected: `400 Bad Request`.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

5. **Create review with invalid user_id**  
   - *Description:* Attempt to create a review with a non-existent `user_id`.  
   - Expected: `404 Not Found`.  
   - Actual: `404 Not Found`.  
   - Status: Pass

6. **Create review with invalid place_id**  
   - *Description:* Attempt to create a review with a non-existent `place_id`.  
   - Expected: `404 Not Found`.  
   - Actual: `404 Not Found`.  
   - Status: Pass

7. **Get review not found**  
   - *Description:* Retrieve a review by a non-existent ID.  
   - Expected: `404 Not Found`.  
   - Actual: `404 Not Found`.  
   - Status: Pass

8. **Update review success**  
   - *Description:* Update an existing review with valid data.  
   - Expected: `200 OK` and updated review data.  
   - Actual: `200 OK`.  
   - Status: Pass

9. **Update review with empty text**  
   - *Description:* Attempt to update a review’s text to an empty string.  
   - Expected: `400 Bad Request`.  
   - Actual: `400 Bad Request`.  
   - Status: Pass

10. **Update review not found**  
    - *Description:* Attempt to update a review by a non-existent ID.  
    - Expected: `404 Not Found`.  
    - Actual: `404 Not Found`.  
    - Status: Pass

11. **Delete review success**  
    - *Description:* Delete an existing review and verify deletion.  
    - Expected: `200 OK` on delete, `404 Not Found` when fetching deleted review.  
    - Actual: `200 OK` and `404 Not Found`.  
    - Status: Pass


## 6. Test Execution Summary

| Test Suite       | Number of Tests | Expected Outcome           | Actual Outcome             | Status  |
|------------------|-----------------|---------------------------|----------------------------|---------|
| User Endpoints   | 7               | Correct HTTP status codes and data validation responses | All tests passed with correct responses | Passed  |
| Place Endpoints  | 11              | Validate creation, update, lat/lon ranges, and errors   | All tests passed as expected                  | Passed  |
| Review Endpoints | 11              | Validate foreign keys, create/update/delete workflows   | All tests passed and edge cases handled       | Passed  |
| Amenity Endpoints| 7               | Validate creation, empty field errors, updates          | All tests passed and validation enforced      | Passed  |

- **Total tests run:** 36  
- **Total tests passed:** 36  
- **Total tests failed:** 0  

## 7. Issues Encountered  

1. **TypeError: `__init__()` missing required argument 'name'**  
   - Caused by incomplete data passed to Amenity constructor.  
   - Fixed by adding validation to ensure required fields exist before creation.

2. **Persistent test data caused unexpected results**  
   - Data was not cleared between tests, leading to false positives/failures.  
   - Fixed by clearing in-memory repositories in the `setUp()` method of tests.

3. **Update endpoints missing input validation**  
   - Updates with empty or invalid fields sometimes returned 200 OK instead of 400 Bad Request.  
   - Fixed by adding strict validation in PUT endpoints.

4. **Incorrect routing causing 400 instead of 404 errors**  
   - Some update tests failed because routes were improperly registered due to nested resource classes.  
   - Fixed by correcting route registration and class placement.

5. **Typo in email validation code causing runtime errors**  
   - Incorrect `.lower*()` method call caused AttributeError.  
   - Fixed by correcting to `.lower()`.

## 8. Test Data Setup and Teardown  

- Each test class uses `setUp` method to initialize Flask app and test client.  
- In-memory repositories are cleared before tests (`facade.<repo>_repo._storage.clear()`).  
- Test users and places created as needed for foreign key references.


## 9. Conclusion

The unit testing suite thoroughly covers CRUD operations and input validation for all main entities (Users, Places, Reviews, Amenities) of the HBnB API. All tests passed successfully, indicating the implementation meets the expected behavior and handles both standard and edge cases well.

The issues identified during testing led to important validation and routing fixes, improving robustness and API reliability. Future testing can expand to integration and performance tests, including testing with persistent databases.

Overall, the project demonstrates solid functionality and quality assurance practices through comprehensive automated testing.

## 10. References  

- [HBnB API Documentation](https://github.com/Holberton-Uy/hbnb-doc)  
- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)  
- [Flask Testing docs](https://flask.palletsprojects.com/en/2.3.x/testing/)
