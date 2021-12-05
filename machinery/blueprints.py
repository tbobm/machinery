"""Flask Blueprints for machinery."""
from flask import request, current_app, Blueprint

from machinery.db import store_service, store_workflow, fetch_workflow_config

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


@common.route('/w', methods=['POST'])
def register_workflow():
    """Validate the JSON payload and store the Workflow in the Database."""
    if not request.is_json:
        return {"message": "json is expected"}, 415

    payload = request.get_json()
    if payload is None:
        return {"message": "payload can not be empty"}, 400

    mongo = current_app.config['db']
    # TODO: ensure every Service listed is defined
    created, infos = store_workflow(payload, mongo.cx)
    if created:
        return infos, 201
    return infos, 409


@common.route('/e/<string:workflow_id>', methods=['POST'])
def process_event(workflow_id: str):
    """Process the event in JSON payload using `workflow_id`."""
    if not request.is_json:
        return {"message": "json is expected"}, 415

    payload = request.get_json()
    if payload is None:
        return {"message": "payload can not be empty"}, 400

    mongo = current_app.config['db']
    _, _ = fetch_workflow_config(workflow_id, mongo.cx)
    return {"message": "found configuration"}, 200
