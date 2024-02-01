#!/usr/bin/python3
""" Script that start a Flask web app
listening port = 0.0.0.0:5000
"""
from flask import Flask, render_template
from models import storage
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/hbnb_filters')
def hbnb_filters():
    """ Display a HTML page: (inside the tag BODY)
    with the list of City related to State if its id exist
    sorted by name(A->Z)"""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template('10-hbnb_filters.html',
                           states=states, amenities=amenities)


@app.teardown_appcontext
def close_down(self):
    """ Removes the current SQLAlchemy Session: """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
