"""DB entities."""
import enum
import typing

from bson.objectid import ObjectId
from marshmallow import ValidationError
import pymongo
import pymongo.errors

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
    all_services_exist = services_exists(result["services"], mongo_client)
    if not all_services_exist:
        # TODO: give more detail regarding the failing services
        return False, {"message": "not all services exist"}
    cursor = mongo_client.get_default_database()
    try:
        result = cursor[MachineryCollections.WORKFLOW.value].insert_one(result)
        workflow_id = result.inserted_id
    except pymongo.errors.DuplicateKeyError:
        result.pop('_id')  # do not edit the `_id` field
        result = cursor[MachineryCollections.WORKFLOW.value].find_one_and_update(
            {'name': result['name']},
            {'$set': result},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        workflow_id = result['_id']
    return True, {'workflow_id': f"{workflow_id}"}


def services_exists(services: typing.List[typing.Union[str, ObjectId]],
                    mongo_client, qualifier='name') -> bool:
    """Lookup a list of `services` in the Database.

    The `qualifier` variable defines the service's name to lookup, either
    by name or service_id (`_id` in the Database).

    Return `True` if all the services are found, `False` otherwise.
    """
    _mapping = {
        'name': str,
        'service_id': ObjectId,
    }
    if qualifier not in _mapping:
        raise ValueError(f'service lookup is available to {",".join(_mapping.keys())}')
    database = mongo_client.get_default_database()
    to_find = set(services)  # a service can be called multiple times
    selector = {
        '$in': [
            _mapping[qualifier](service_identifier)
            for service_identifier in to_find
        ]
    }
    _query = {
        qualifier: selector
    }
    documents = database[MachineryCollections.SERVICE.value].distinct(
        qualifier,
        _query,
    )
    return len(set(documents)) == len(to_find)


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
    try:
        result = cursor[MachineryCollections.SERVICE.value].insert_one(result)
        service_id = result.inserted_id
    except pymongo.errors.DuplicateKeyError:
        result.pop('_id')  # do not edit the `_id` field
        result = cursor[MachineryCollections.SERVICE.value].find_one_and_update(
            {'name': result['name']},
            {'$set': result},
            return_document=pymongo.ReturnDocument.AFTER,
        )
        service_id = result['_id']
    return True, {'service_id': f"{service_id}"}
