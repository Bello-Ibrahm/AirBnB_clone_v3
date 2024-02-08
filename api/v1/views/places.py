#!/usr/bin/python3
""" Place module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<string:city_id>/places", methods=['GET', 'POST'],
                 strict_slashes=False)
def handle_http_places_by_id(city_id=None):
    """ Review route to handle http methods
    GET:
        retrieves place by its city_id
    POST:
        Create new place object
    """
    city = storage.get(City, city_id)
    if (city is None):
        abort(404)

    if (request.method == 'GET'):
        place_list_dict = [obj.to_dict() for obj in city.places]
        return jsonify(place_list_dict)

    if (request.method == 'POST'):
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        json_data = request.get_json()
        user_id = json_data.get('user_id')
        name = json_data.get('name')

        city = storage.get(City, city_id)
        if city is None:
            abort(404)
        if not user_id:
            return make_response(jsonify({"error": "Missing user_id"}), 400)
        if not name:
            return make_response(jsonify({"error": "Missing name"}), 400)

        json_data['city_id'] = city_id
        user = storage.get(User, user_id)
        if user is None:
            abort(404)
        obj = Place(**json_data)
        obj.save()
        return (jsonify(obj.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def handle_http_place_by_id(place_id=None):
    """ Review route to handle http methods
    GET:
        retrieves place by its place_id
    DELETE:
        deletes place by its place_id
    PUT:
        updates place object by its id
    """
    place_dct = storage.get(Place, place_id)
    if (place_dct is None):
        abort(404)

    if (request.method == 'GET'):
        return jsonify(place_dct.to_dict())

    if (request.method == 'DELETE'):
        place = storage.get(Place, place_id)
        if (place is None):
            abort(404)
        place.delete()
        storage.save()
        return jsonify({})

    if (request.method == 'PUT'):
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        place_obj = storage.get(Place, place_id)
        if (place_obj is None):
            abort(404)
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(place_obj, key, value)
        storage.save()
        return jsonify(place_obj.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search_post():
    """ searches for a place """
    if request.get_json() is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
