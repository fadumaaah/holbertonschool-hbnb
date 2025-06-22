# app/api/reviews.py
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace("reviews", description="Review operations")

review_model = api.model("Review", {
    "id":       fields.String(readOnly=True),
    "text":     fields.String(required=True, description="Review text"),
    "user_id":  fields.String(required=True, description="Author id"),
    "place_id": fields.String(required=True, description="Place id")
})

def _to_response(review):
    return {
        "id":   review.id,
        "text": review.text,
        "user": {
            "id": review.user.id,
            "email": review.user.email
        },
        "place_id": review.place.id,
        "created_at": review.created_at.isoformat(),
        "updated_at": review.updated_at.isoformat()
    }

@api.route("/")
class ReviewList(Resource):
    @api.expect(review_model, validate=True)
    @api.response(201, "Review created")
    @api.response(400, "Bad input")
    def post(self):
        try:
            rev = facade.create_review(api.payload)
            return _to_response(rev), 201
        except ValueError as err:
            return {"error": str(err)}, 400

@api.route("/<review_id>")
class ReviewResource(Resource):
    @api.response(200, "Found")
    @api.response(404, "Not found")
    def get(self, review_id):
        rev = facade.get_review(review_id)
        if not rev:
            return {"error": "Review not found"}, 404
        return _to_response(rev), 200

    @api.expect(review_model, validate=True)
    @api.response(200, "Updated")
    @api.response(404, "Not found")
    @api.response(400, "Bad input")
    def put(self, review_id):
        try:
            rev = facade.update_review(review_id, api.payload)
            if not rev:
                return {"error": "Review not found"}, 404
            return {"message": "Review updated"}, 200
        except ValueError as err:
            return {"error": str(err)}, 400

    @api.response(204, "Deleted")
    @api.response(404, "Not found")
    def delete(self, review_id):
        ok = facade.delete_review(review_id)
        if not ok:
            return {"error": "Review not found"}, 404
        return "", 204


@api.route("/place/<place_id>")
class ReviewsByPlace(Resource):
    @api.response(200, "OK")
    @api.response(404, "Place not found")
    def get(self, place_id):
        reviews = facade.get_reviews_for_place(place_id)
        if reviews is None:
            return {"error": "Place not found"}, 404
        return [_to_response(r) for r in reviews], 200
