"""Basic service to count the number of space."""
import os

import flask


def get_informations():
    """
    Get all space-counter service informations and return 
    them formated into a dict.
    :return: all informations about the space_counter service.
    :rtype: dict
    """
    informations = {
        "name": "space-counter",
        "address": "http://space-counter.local:5000/",
        "inputs": [
            {
                "name": "message",
                "type": "string",
                "description": "The text to analyze"
            }
        ],
        "outputs": [
            {
                "name": "message",
                "type": "string",
                "description": "The number of spaces in the text"
            }
        ]
    }
    return informations


def create_app():
    """
    Configure a Flask instance for space-counter service.
    :return: a configured flask instance.
    :rtype: flask.Flask()
    """
    app = flask.Flask(__name__)

    @app.route('/healthcheck')
    def healthcheck():
        """
        Dumb route to check if the server is running.
        :return: "204 NO CONTENT".
        :rtype: flask.Response
        """
        return flask.Response(status=204)

    @app.route('/infos')
    def infos():
        """
        Get informations about the space_counter service, like
        name, expected inputs & outputs, url, etc.
        :return: "200 OK" with informations.
        :rtype: flask.Response
        """
        infos = get_informations()
        res = flask.make_response(infos)
        res.status = 200
        return res

    @app.route('/event', methods=['POST'])
    def event():
        """
        Count the number of spaces into a given message.
        :return: "200 OK" with the number of spaces, or 
        "4xx" appropriate code with error message
        :rtype: flask.Response
        """
        req = flask.request

        if not req.is_json:
            res = flask.make_response({
                'message': 'JSON is expected.'
            })
            res.status = 415
            return res

        payload: dict = req.get_json()
        if not payload:
            res = flask.make_response({
                'message': 'payload can not be empty.'
            })
            res.status = 400
            return res
            
        message: str = payload.get('message')
        if not message:
            res = flask.make_response({
                'message': 'message field is missing on payload.'
            })
            res.status = 400
            return res

        res = flask.make_response({'message': message.count(" ")})
        res.status = 200
        return res

    return app


def main():
    """Start the Flask application."""
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', "5000")))


if __name__ == "__main__":
    main()

