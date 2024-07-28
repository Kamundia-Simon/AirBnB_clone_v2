#!/usr/bin/python3
"""
flask web with 5 routes
"""
from flask import Flask
from flask import render_template
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """
    Route handler for the root URL.
    Returns:
        str: message "Hello HBNB!"
    """
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """
    Route handler for the '/hbnb' URL.
    Returns:
        str: message "HBNB"
    """
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def c(text):
    """Displays 'C' followed by the value of <text>."""
    text = text.replace('_', ' ')
    return "C {}".format(text)


@app.route("/python", defaults={'text': 'is cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text):
    """Displays 'Python' followed by the value of <text>.

    Replaces any _ in <text> with /.
    """
    text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """display 'n is a number' only if n is an int"""
    return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n):
    """Displays an HTML page only if <n> is an integer."""
    return render_template("5-number.html", n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
