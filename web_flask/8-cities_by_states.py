#!/usr/bin/python3
""" Script that start a Flask web app
listening port = 0.0.0.0:5000
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/cities_by_states')
def cities_by_states():
    """ Display a HTML page: (inside the tag BODY
    with the list of City objects linked to the State
    sorted by name(A->Z)"""
    states = storage.all(State)
    return render_template('8-cities_by_states.html', states=states)


@app.teardown_appcontext
def close_down(self):
    """ Removes the current SQLAlchemy Session: """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
