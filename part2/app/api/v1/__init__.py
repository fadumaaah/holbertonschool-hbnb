from app.api.places import api as places_ns
api.add_namespace(places_ns, path="/places")