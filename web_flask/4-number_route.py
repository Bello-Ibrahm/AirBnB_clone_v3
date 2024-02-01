#!/usr/bin/python3
""" Script that start a Flask web app
listening port = 0.0.0.0:5000
"""
from flask import Flask
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """ Display Hello HBNB! """
    return ("Hello HBNB!")


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """ Display HBNB """
    return ("HBNB")


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """ Display “C ” followed by the value of the text variable
    (replace underscore _ symbols with a space )
    """
    return ("C {:s}".format(text).replace('_', ' '))


@app.route('/python', strict_slashes=False)
@app.route('/python/<text>', strict_slashes=False)
def python(text="is cool"):
    """ Display “Python ”, followed by the value of the text variable """
    return ("Python {:s}".format(text).replace('_', ' '))


@app.route('/number/<int:n>', strict_slashes=False)
def isNumber(n):
    """ Display “n is a number” only if n is an integer """
    return ("{} is a number".format(n) if isinstance(n, int) else "")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)
