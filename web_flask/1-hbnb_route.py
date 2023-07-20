#!/usr/bin/python3
"""
 This module contains script that starts a Flask web application:

 The web application must be listening on 0.0.0.0, port 5000
 Routes:
 /: display “Hello HBNB!”
 /hbnb: display "HBNB"
 You must use the option strict_slashes=False in your route definition
 """

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def hello_hbnb():
    """Display Hello HBNB"""
    return "Hello HBNB"


@app.route("/hbnb")
def hbnb():
    """Display HBNB"""
    return "HBNB"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
