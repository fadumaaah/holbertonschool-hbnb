# HBnB Evolution

## Table of Contents

- [Introduction](#introduction)
- [1. High-Level Architecture](#1-high-level-architecture)
- [2. Business Logic Layer](#2-business-logic-layer)
- [3. API Interaction Flow](#3-api-interaction-flow)
- [Conclusion](#conclusion)
- [Authors](#authors)

## Introduction
This document serves as the technical foundation for the HBnB project, a platform designed for users to find, book, and review short-term rental properties. The goal of the HBnB system is to provide a smooth and reliable experience for both guests and hosts, supporting features like user registration, place listings, bookings, reviews, and amenity management.

The purpose of this document is to outline the system’s architecture and design through diagrams and explanations. It includes a high-level overview of the system, detailed class structures for core components, and interaction flows for key API calls.

By bringing all of this together, the document will guide the implementation phase, help maintain consistency across development, and serve as an ongoing reference for the technical direction of the project.



## 1. High-Level Architecture:


## 2. Business Logic Layer:
![Class Diagram](/diagrams/class_uml.png)
The class diagram provides a clear overview of the core entities in the business logic layer—such as User, Place, Review, and Amenity—and how they relate to each other. It supports modular design, making the system easier to develop, maintain, and scale. This diagram fits into the overall architecture by defining the structure and rules that guide how data is processed between the API layer and the database.
### Base Model<br>
Parent class that provides common attributes and functionality for all other classes in the system <br>

**Attributes**
- `id:uuid` - Unique Identifier.<br>
- `created_at: DateTime` - Creation timestamp<br>
- `updated_at: DateTime` - Last update timestamp<br>

**Methods**
- `__init__` - Initializes a new instance with default or provided values
- `save()` - Save the object to the database<br>
- `delete()` - Delete the object from the database<br>
- `to_dict()` - Return a dictionary representation of the object


### 👤 User<br>
Represents a user on the platform who can book places, write reviews, manage their profile and create listings.<br>

**Attributes**
- `first_name: string`<br>
- `last_name: string`<br>
- `email: string`<br>
- `password: string`<br>

**Methods**
- `login()` - Log the user into the system.<br>
- `authenticate()` - Verify user login credentials<br>
- `register()` - Register a new user.<br>
- `update_profile()` - Update user details<br>
- `add_review` - Submit a review for a place.<br>
- `get_bookings` - Retrieve all bookings by the user.<br>

### 🏠 Place
Represents a property listed on the platform that users can view, book, and review.

**Attributes**
- `name: string`
- `description: string`
- `price: float`
- `latitude: float`
- `longitude: float`
- `is_available: bool`
- `max_guests: int`
- `num_bedrooms: int`

**Methods**
- `check_availability()` - Check if the place is available for a given date range.
- `add_booking()` - Add a new booking for the place.
- `update_details()` - Update the place's information (name, description, price, etc.).

### 📝 Review
Represents feedback left by a user for a specific place, including a rating.

**Attributes**
- `place_id: uuid`
- `rating: int`
- `response: str (optional)`

**Methods**
- `calc_average_rating()` - Calculate and return the average rating for the associated place.
- `add_review()` - Submit a new review for a place.
- `update_review()` - Update the rating and/or response of an existing review.

### ✨ Amenity
Represents a feature or service available at a place (e.g., Wi-Fi, parking, pool).

**Attributes**
- `name: string`
- `description: string`

**Methods**
- `update_amenity()` — Update the name and/or description of the amenity.

### 📅 Booking
Represents a reservation made by a user for a specific place during a defined date range.

**Attributes**
- `user_id: uuid`
- `place_id: uuid`
- `check_in: date`
- `check_out: date`
- `status: string`
- `total_price: float` 

**Methods**
- `update_status(new_status)` — Update the booking status (e.g., confirmed, cancelled).
- `calculate_total_price()` — Calculate the total price based on place price and duration.
- `cancel_booking()` — Cancel the booking and update status accordingly.

### 🌆 City  
Represents a city where places can be located.

**Attributes**
- `name: string`  
- `latitude: float`  
- `longitude: float`  
- `timezone: string` 

**Methods**  
*(Inherits from BaseModel — no city-specific methods)*

### Relationships
- A **User** can have many **Bookings**, each booking belongs to one user.  
- A **User** can write many **Reviews**, each review is authored by one user.  
- A **Place** can have many **Bookings**, each booking is for one place.  
- A **Place** can have many **Reviews**, each review relates to one place.  
- A **Place** can have many **Amenities**, and an **Amenity** can belong to many places (many-to-many).  
- A **Place** belongs to one **City**, while a city can have many places.  

## 3. API Interaction Flow:

  🔁 **User Registration** 

A user signs up for a new account

![User Registration](/diagrams/user_registration.png)

1. **User Action**: Sends `POST /users/register` with name, email, and password.
2. **API Layer**: Validates input (e.g. required fields, email format) and forwards to Business Logic.
3. **Business Logic**: Checks for existing email, hashes password, calls `inputUser(userData)`.
4. **Database**: Inserts user record, returns result.
5. **User Response**: Returns a success message or an appropriate error based on the outcome.
   - `201 Created`  
   `{ "message": "Account created successfully." }`
   - `400 Bad Request` - Missing or Invalid fields  
   `{ "error": "Email and password are required." }`
   - `409 Conflict` - Duplicate account  
   `{ "error": "An account with this email already exists." }`

 🔁 **Place Creation** 

![Place Creation](/diagrams/place_creation.png)

A user creates a new place listing

1. **User Action**: Submits place details (title, location, price, etc.).
2. **API Layer**: Validates input, checks authentication, and forwards request to Business Logic.
3. **Business Logic**: Prepares data and calls `insertPlace()`.
4. **Database**: Inserts the new place record and returns a result.
5. **User Response**: Returns a success message or an appropriate error based on the outcome.
   - `201 Created`  
     `{ "id": "12345", "message": "Place created successfully" }`
   - `400 Bad Request` – Missing or invalid fields  
     `{ "error": "Title, location, and price are required." }`
   - `401 Unauthorized` – User not authenticated  
     `{ "error": "Authentication required." }`

 🔁 **Review Submission**  

![Review Submission](/diagrams/review_submission.png)

A user submits a review for a place.

1. **User Action**: Sends `POST /places/{id}/reviews` with rating and comment.
2. **API Layer**: Validates input (e.g. required fields, data types), checks authentication, and forwards to Business Logic.
3. **Business Logic**: Verifies place exists, confirms user booking, and calls `insertReview(reviewData)`.
4. **Database**: Inserts review record, returns result.
5. **User Response**: Returns a success message or an appropriate error based on the outcome.
   - `201 Created`  
     `{ "message": "Your review has been posted successfully!" }`  
   - `400 Bad Request` – Missing or invalid fields  
     `{ "error": "Review text and rating are required." }`  
   - `403 Forbidden` – User not allowed to review  
     `{ "error": "Only users who booked this place can submit reviews." }`


 🔁 **Fetching a List of Places** 

![Fetch List of Places](/diagrams/fetch_list.png)

A user browses available listings based on filter criteria.
1. **User Action**: Sends `GET /places?filters=...` to retrieve places based on filters (e.g., location or price).
2. **API Layer**: Receives the request and forwards the filters to the Business Logic layer.  
3. **Business Logic Layer**: Processes the filters, builds a query, and calls `fetchPlaces()` to retrieve results.  
4. **Database**: Executes the query and returns the matching place listings.  
5. **User Response**: Returns a success message or an appropriate error based on the outcome.
    - `200 OK` – Returns structured list of matching places.  
   - `400 Bad Request`  
   `{ "error": "Invalid filter parameters." }`  
   - `500 Internal Server Error`  
   `{ "error": "Could not fetch places at this time." }`

## Conclusion
This document brings together the core design and architecture of the HBnB project to support a smooth development process. It will be regularly updated as the project evolves, ensuring the team stays aligned and informed throughout implementation.

## Authors
Kassandra Iatrou  
Faduma Abdihashi  
Alex Atanasovski
