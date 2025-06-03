


# HBnB Evolution

### Table of Contents


## High-Level Architecture:


## Business Logic Layer:
![My Photo](/diagrams/class_uml.png)
### Base Model<br>
Parent class that provides common attributes and functionality for all other classes in the system <br>

**Attributes**
- `id:uuid` - Unique Identifier.<br>
- `created_at: DateTime` - Creation timestamp<br>
- `updated_at: DateTime` - Last update timestamp<br>

**Methods**
- `__init__` - Initalizes a new instance with default or provided values
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
- `update_profile()` - Update user detals<br>
- `add_review` - Submit a review for a place.<br>
- `get_bookings` - Retreive all bookings by the user.<br>

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
- Each **Review** links one **User** (author) to one **Place** (subject).


## API Interaction Flow:

## Conclusion
## Authors
Kassandra Iatrou  
Faduma Abdihashi   
Alex Atanasovski
