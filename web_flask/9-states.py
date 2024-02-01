#!/usr/bin/python3
""" Script that start a Flask web app
listening port = 0.0.0.0:5000
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states')
def states():
    """ Display a HTML page: (inside the tag BODY
    with the list of States in the database
    sorted by name(A->Z)"""
    states = storage.all(State)
    return render_template('9-states.html', states=states, mode='all_records')


@app.route('/states/<id>')
def states_by_id(id):
    """ Display a HTML page: (inside the tag BODY)
    with the list of City related to State if its id exist
    sorted by name(A->Z)"""
    states = storage.all(State).values()
    for state in states:
        if (state.id == id):
            return render_template('9-states.html', states=state, mode='by_id')
    return render_template('9-states.html', mode='None')


@app.teardown_appcontext
def close_down(self):
    """ Removes the current SQLAlchemy Session: """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
