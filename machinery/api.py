"""Main module."""
import os

import flask

app = flask.Flask(__name__)


@app.route('/healthcheck')
def healthcheck():
    """Simply return OK."""
    return 204


def main():
    """Start the Flask application."""
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', "5000")))


if __name__ == "__main__":
    main()
