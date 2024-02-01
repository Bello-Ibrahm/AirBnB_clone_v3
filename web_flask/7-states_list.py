#!/usr/bin/python3
""" Script that start a Flask web app
listening port = 0.0.0.0:5000
"""
from flask import Flask, render_template
from models import storage
from models.state import State
app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route('/states_list')
def states_list():
    """ Display a HTML page: (inside the tag BODY
    with the list of all State objects
    present in DBStorage sorted by name (A->Z)"""
    states = storage.all()
    return render_template('7-states_list.html', states=states)


@app.teardown_appcontext
def close_down(self):
    """ Removes the current SQLAlchemy Session: """
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
