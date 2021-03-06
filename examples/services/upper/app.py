"""Basic service to transform a text to uppercase."""
import os

import flask


def get_informations():
    """
    Get all upper service informations and return them 
    formated into a dict.
    :return: all informations about the upper service.
    :rtype: dict
    """
    informations = {
        "name": "upper",
        "address": "http://upper.local:5000/",
        "inputs": [
            {
                "name": "message",
                "type": "string",
                "description": "The text to transform"
            }
        ],
        "outputs": [
            {
                "name": "message",
                "type": "string",
                "description": "The transformed text, in uppercase"
            }
        ]
    }
    return informations


def create_app():
    """
    Configure a Flask instance for upper service.
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
        Get informations about the upper service, like
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
        Transform a given message to uppercase.
        :return: "200 OK" with tranformed message, or 
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
        
        res = flask.make_response({'message': message.upper()})
        res.status = 200
        return res

    return app


def main():
    """Start the Flask application."""
    app = create_app()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', "5000")))


if __name__ == "__main__":
    main()

