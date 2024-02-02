#!/usr/bin/python3
"""
App module
"""
from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.register_blueprint(app_views)
HBNB_API_HOST = getenv('HBNB_API_HOST', default='0.0.0.0')
HBNB_API_PORT = int(getenv('HBNB_API_PORT', default=5000))


@app.errorhandler(404)
def not_found(error):
    """ json 404 page """
    return make_response(jsonify({"error": "Not found"}), 404)


@app.teardown_appcontext
def close_db_session(obj):
    """ calls the close() """
    storage.close()


if __name__ == "__main__":
    """ Run the app =>  python -m api.v1.app  """
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
