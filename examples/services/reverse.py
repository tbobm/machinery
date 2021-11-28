"""Basic service to reverse a message."""
import os

import flask


def get_reverse_informations():
    """
    Get all reverse service informations and return 
    them formated into a dict.
    :return: all informations about the reverse service.
    :rtype: dict
    """
    informations = {
        "name": "reverse",
        "address": "http://reverse.local:5000/",
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
                "description": "The reversed text"
            }
        ]
    }
    return informations


def create_reverse():
    """
    Configure a Flask instance for reverse service.
    :return: a configured flask instance.
    :rtype: flask.Flask()
    """
    reverse = flask.Flask(__name__)

    @reverse.route('/healthcheck')
    def healthcheck():
        """
        Dumb route to check if the server is running.
        :return: "204 NO CONTENT".
        :rtype: flask.Response
        """
        return flask.Response(status=204)

    @reverse.route('/infos')
    def infos():
        """
        Get informations about the reverse service, like
        name, expected inputs & outputs, url, etc.
        :return: "200 OK" with informations.
        :rtype: flask.Response
        """
        infos = get_reverse_informations()
        res = flask.make_response(infos)
        res.status = 200
        return res

    @reverse.route('/event', methods=['POST'])
    def event():
        """
        Reverse the given message.
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

        res = flask.make_response({'message': message[::-1]})
        res.status = 200
        return res

    return reverse


def main():
    """Start the Flask application."""
    reverse = create_reverse()
    reverse.run(host='0.0.0.0', port=int(os.environ.get('REVERSE_PORT', "5000")))


if __name__ == "__main__":
    main()

