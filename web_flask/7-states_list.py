#!/usr/bin/python3
"""
Flask web app to display list of states
"""

from flask import Flask, render_template
from models import storage


app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Displays an HTML page with a list of all State objects in DBStorage
    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exception):
    """Removes current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(debug=True)
