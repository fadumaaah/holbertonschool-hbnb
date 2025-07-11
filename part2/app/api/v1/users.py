#!/usr/bin/python3

from flask_restx import Namespace, Resource, fields
from app.services import facade
from app.models.user import User


api = Namespace("users", description="User operations")

user_model = api.model("User", {
    "first_name": fields.String(required=True, description="First name of user"),
    "last_name": fields.String(required=True, description="Last name of the user"),
    "email": fields.String(required=True, description="Email of the user")
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, "User successfully created")
    @api.response(400, "Email already registered or invalid input data")
    def post(self):
        user_data = api.payload
        email = user_data.get("email", "").strip().lower()
        try:
            existing_user = facade.get_user_by_email(email)
            if existing_user:
                return {"error": "Email already registered"}, 400
            
            user_data["email"] = email 
            new_user = facade.create_user(user_data)
            return {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
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


@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Email already registered or invalid input data')
    def put(self, user_id):
        data = api.payload
        try:
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404

            if 'email' in data:
                new_email = data['email'].strip().lower()
                if new_email != user.email.strip().lower():
                    existing_user = facade.get_user_by_email(new_email)
                    if existing_user:
                        return {'error': 'Email already registered'}, 400
                data['email'] = new_email

            updated_user = facade.update_user(user_id, data)
            if updated_user is None:
                return {'error': 'User not found'}, 404

            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception:
            return {'error': 'Invalid input data'}, 400
