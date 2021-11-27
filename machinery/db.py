"""DB entities."""
import enum
import typing

from marshmallow import ValidationError
import pymongo

from machinery.entity import WorkflowSchema


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
    return inserted.acknowledged, {'workflow_id': inserted.inserted_id}
