from flask_restx import Namespace, Resource, fields
from app.services import facade

# So i'm trying something new here, Saw some people do something similar to this, which is a "helper" function
# which should help to convert a Place model instance to a response dictionary. (allowing us to link reviews if im not wrong)
def place_to_response(place, expand_reviews=False):
    data = place.to_dict()   # basic fields from BaseModel
    if expand_reviews:
        data["reviews"] = [
            {
                "id":     r.id,
                "text":   r.text,
                "rating": r.rating,
                "user": {
                    "id":    r.user.id,
                    "email": getattr(r.user, "email", None)  # guard if email not on model
                }
            } for r in place.reviews
        ]
    return data

# Since we added multiple inputs like number_rooms, I created a helper function to exclude any variables with null values from the response, ensuring only meaningful data is displayed.
def clean_nulls(data: dict) -> dict:
    return {k: v for k, v in data.items() if v is not None}

api = Namespace("places", description="Place operations")

amenity_id_field = fields.String(description="Amenity id")

place_model = api.model(
    "Place",
    {
        "id": fields.String(readOnly=True, description="Unique id"),
        "title": fields.String(required=True, description="Place title"),
        "description": fields.String(description="Description"),
        "city_id": fields.String(description="City id"),
        "owner_id": fields.String(required=True, description="Owner (user) id"),
        "number_rooms": fields.Integer(min=0, description="# rooms"),
        "number_bathrooms": fields.Integer(min=0, description="# bathrooms"),
        "max_guest": fields.Integer(min=0, description="Max guests"),
        "price": fields.Float(min=0, description="Price (cents)"),
        "latitude": fields.Float(description="Latitude"),
        "longitude": fields.Float(description="Longitude"),
        "amenities": fields.List(amenity_id_field, description="List of amenity ids"),
    },
)

# Second model for when we update place - above has required fields that is for post.
place_update_model = api.model(
    "PlaceUpdate",
    {
        "title": fields.String(description="Place title"),
        "description": fields.String(description="Description"),
        "city_id": fields.String(description="City id"),
        "owner_id": fields.String(description="Owner (user) id"),
        "number_rooms": fields.Integer(min=0, description="# rooms"),
        "number_bathrooms": fields.Integer(min=0, description="# bathrooms"),
        "max_guest": fields.Integer(min=0, description="Max guests"),
        "price": fields.Float(min=0, description="Price (cents)"),
        "latitude": fields.Float(description="Latitude"),
        "longitude": fields.Float(description="Longitude"),
        "amenities": fields.List(fields.String, description="List of amenity ids"),
    },
)


@api.route("/")
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, "Place created")
    @api.response(400, "Bad input")
    def post(self):
        """Create a new place"""
        try:
            new_place = facade.create_place(api.payload)
            data = clean_nulls(new_place.to_dict())
            return data, 201
        except ValueError as err:
            return {"error": str(err)}, 400

    @api.response(200, "Success")
    def get(self):
        """Return *all* places"""
        places = facade.get_all_places()
        cleaned_places = [clean_nulls(p.to_dict()) for p in places]
        return cleaned_places, 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    @api.response(200, "Found")
    @api.response(404, "Not found")
    def get(self, place_id):
        """Get one place by id"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        data = clean_nulls(place.to_dict())
        return data, 200

    @api.expect(place_update_model, validate=True)
    @api.response(200, "Updated")
    @api.response(404, "Not found")
    @api.response(400, "Bad input")
    def put(self, place_id):
        """Update an existing place (no delete in this milestone)"""
        try:
            updated = facade.update_place(place_id, api.payload)
            if not updated:
                return {"error": "Place not found"}, 404
            return {"message": "Place updated"}, 200
        except ValueError as err:
            return {"error": str(err)}, 400
