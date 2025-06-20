from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("places", description="Place operations")

amenity_id_field = fields.String(description="Amenity id")

place_model = api.model(
    "Place",
    {
        "id": fields.String(readOnly=True, description="Unique id"),
        "name": fields.String(required=True, description="Place name"),
        "description": fields.String(description="Description"),
        "city_id": fields.String(required=True, description="City id"),
        "user_id": fields.String(required=True, description="Owner (user) id"),
        "number_rooms": fields.Integer(min=0, description="# rooms"),
        "number_bathrooms": fields.Integer(min=0, description="# bathrooms"),
        "max_guest": fields.Integer(min=0, description="Max guests"),
        "price_by_night": fields.Integer(min=0, description="Price (cents)"),
        "latitude": fields.Float(description="Latitude"),
        "longitude": fields.Float(description="Longitude"),
        "amenity_ids": fields.List(amenity_id_field, description="List of amenity ids"),
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
            return api.marshal(new_place.to_dict(), place_model), 201
        except ValueError as err:
            return {"error": str(err)}, 400

    @api.response(200, "Success")
    def get(self):
        """Return *all* places"""
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    @api.response(200, "Found")
    @api.response(404, "Not found")
    def get(self, place_id):
        """Get one place by id"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(expand=True), 200

    @api.expect(place_model, validate=True)
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
