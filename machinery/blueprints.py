"""Flask Blueprints for machinery."""
from flask import request, current_app, Blueprint

from machinery.db import store_service


common = Blueprint('api', __name__)


@common.route('/s', methods=['POST'])
def register_service():
    """Validate the JSON payload and store the Service in the Database."""
    if not request.is_json:
        return {"message": "json is expected"}, 415

    payload = request.get_json()
    if payload is None:
        return {"message": "payload can not be empty"}, 400

    mongo = current_app.config['db']
    created, infos = store_service(payload, mongo.cx)
    if created:
        return infos, 201
    return infos, 409
