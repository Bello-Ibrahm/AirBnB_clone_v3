#!/usr/bin/python3
""" Place Amenities module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage, storage_type
from models.amenity import Amenity
from models.place import Place


@app_views.route("/places/<string:place_id>/amenities", methods=['GET'],
                 strict_slashes=False)
def get_all_amenities(place_id=None):
    """ Retrieves all amenities by its place_id
    """
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)
    amenities_list_dict = [obj.to_dict() for obj in place.amenities]
    return jsonify(amenities_list_dict)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>',
                 methods=['DELETE', 'POST'], strict_slashes=False)
def handle_amenity_method(place_id=None, amenity_id=None):
    """ Review route to handle http methods
    DELETE:
        deletes a Amenity object to a Place
    POST:
        link a Amenity object to a Place
    """
    place = storage.get(Place, place_id)
    if (place is None):
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if (amenity is None):
        abort(404)

    if request.method == 'DELETE':
        if (amenity not in place.amenities and
                amenity.id not in place.amenities):
            abort(404)
        """ if storage_type == 'db':
            place.amenities.remove(amenity)
        else:
            place.amenity_ids.pop(amenity.id, None)
        # place.save()"""
        place.amenities.remove(amenity)
        storage.save()
        return (jsonify({}), 200)

    if request.method == 'POST':
        if (amenity in place.amenities or
                amenity.id in place.amenities):
            return (jsonify(amenity.to_dict()), 200)
        if storage_type == 'db':
            place.amenities.append(amenity)
        else:
            place.amenities = amenity
        return (jsonify(amenity.to_dict()), 201)
