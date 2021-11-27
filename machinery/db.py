"""DB entities."""
import enum
import typing

from marshmallow import ValidationError
import pymongo

from machinery.entity import WorkflowSchema, ServiceSchema


DEFAULT_MONGO_URI = "mongodb://user:password@localhost:27017/machinery?authSource=admin"


class MachineryCollections(enum.Enum):
    """MongoDB Collections for the stored configurations."""
    WORKFLOW = 'machinery_workflows'
    SERVICE = 'machinery_services'


def store_workflow(payload: dict, mongo_client: pymongo.MongoClient) -> typing.Tuple[bool, dict]:
    """Validate and store a valid Workflow `payload`.

    First return parameter defined if the Workflow has been registered.
    Second return parameter is an informative dictionary.
    """
    schema = WorkflowSchema()
    try:
        result = schema.load(payload)
    except ValidationError as err:
        return False, err.messages
    cursor = mongo_client.get_default_database()
    inserted = cursor[MachineryCollections.WORKFLOW.value].insert_one(result)
    return inserted.acknowledged, {'workflow_id': f"{inserted.inserted_id}"}


def store_service(payload: dict, mongo_client: pymongo.MongoClient) -> typing.Tuple[bool, dict]:
    """Validate and store a valid Service `payload`.

    First return parameter defined if the Service has been registered.
    Second return parameter is an informative dictionary.
    """
    schema = ServiceSchema()
    try:
        result = schema.load(payload)
    except ValidationError as err:
        return False, err.messages
    cursor = mongo_client.get_default_database()
    inserted = cursor[MachineryCollections.SERVICE.value].insert_one(result)
    return inserted.acknowledged, {'service_id': f"{inserted.inserted_id}"}
