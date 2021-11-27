"""Main module."""
import os

import flask
from flask_pymongo import PyMongo

from machinery.db import DEFAULT_MONGO_URI
from machinery.blueprints import common


def create_app():
    """Return a configured flask.Flask instance.

    Adds the `PyMongo` instance to the `config['db']` attribute.
    """
    app = flask.Flask(__name__)
    app.config["MONGO_URI"] = os.environ.get('MONGO_URI', DEFAULT_MONGO_URI)
    mongo = PyMongo(app)
    app.config['db'] = mongo

    app.register_blueprint(common)

    @app.route('/healthcheck')
    def healthcheck():
        """Simply return OK."""
        return {}, 204

    return app


def main():
    """Start the Flask application."""
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', "5000")))


if __name__ == "__main__":
    main()
