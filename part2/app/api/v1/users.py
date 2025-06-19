#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.user import User


api = Namespace("users", description="User operations")

# Defines what data the API expects when create/updating users
# Used for - input validation, auto-generating API document and Swagger UI forms
user_model = api.model("User",{
    "first_name": fields.String(required=True, description="First name of user"),
    "last_name": fields.String(required=True, description="Last name of the user"),
    "email": fields.String(required=True, description="Email of the user")
})

# Endpoint at /users/ that handles operations on the user collection
@api.route('/')
class UserList(Resource):
    # validates incoming data against user_model
    @api.expect(user_model, validate=True)
    # documents possibel response for auto-generated docs
    @api.response(201, "User successfully created")
    # handles HTTP POST requests (creating new users)
    @api.response(400, "Email already registered or invalid input data")
    def post(self):
        """
        Register a new user
        """
        # get JSON data sent in the request body
        user_data = api.payload

        try:
            # Check for duplicate email before creating user
            existing_user = facade.get_user_by_email(user_data["email"])
            if existing_user:
                return ({"error": "Email already registered"}, 400)

            # Creates user and returns user data with HTTP status 201 (created)
            new_user = facade.create_user(user_data)

            return ({
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email
            }, 201)

        # error handling - catches validation errors and returns HTPP 400 (bad request)
        except ValueError as e:
            return ({"error": str(e)}, 400)
        except Exception as e:
            return ({"error:" "Invalid input data"}, 400)

    @api.response(200, 'List of users retrieved successfully')
    # gets all users from the database, uses list comprehension to format each user as a dictionary, returns the list with HTTP 200 (ok)
    def get(self):
        """Retrieve list of users"""
        users = facade.get_all_users()

        return [
            {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
            }
             for user in users
        ], 200

    # creates endpoints for operations on specific users
    @api.route('/<user_id>')
    class UserResource(Resource):
        @api.response(200, 'User details retrieved successfully')
        @api.response(404, 'User not found')
        # takes user id from URL, returns user data or 404 (not found) is user doesn't exist
        def get(self, user_id):
            """Get user details by ID"""
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200
    
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered or invalid input data')
    # hadles HTTP PUT requests to update existing users
    def put(self, user_id):
        """Update user by ID"""
        data = api.payload
        
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            # Check for duplicate email if email is being changed
            if 'email' in data and data['email'] != user.email:
                existing_user = facade.get_user_by_email(data['email'])
                if existing_user:
                    return {'error': 'Email already registered'}, 400

            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                return {'error': 'User not found'}, 404
    
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
            
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Invalid input data'}, 400