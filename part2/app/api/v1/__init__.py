# This is the only one that I'm confused about, not sure if its correct -- Alex

from app.api.places import api as places_ns
api.add_namespace(places_ns, path="/places")

from app.api.reviews import api as reviews_ns
api.add_namespace(reviews_ns, path="/reviews")