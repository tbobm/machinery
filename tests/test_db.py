"""Storage-related unittests."""
import pytest

from bson.objectid import ObjectId
from machinery import db


def test_insert_workflow(valid_workflow, db_client):
    """Ensure a Valid Workflow can be inserted in the proper Collection."""
    workflow = {
        **valid_workflow,
        **{'name': 'valid-insert'},
    }
    created, data = db.store_workflow(workflow, db_client)
    assert created is True
    assert 'workflow_id' in data
    database = db_client.get_default_database()
    query = {"_id": ObjectId(data['workflow_id'])}
    doc = database[db.MachineryCollections.WORKFLOW.value].find_one(query)
    assert doc['name'] == workflow['name']


def test_insert_workflow_failed(bad_generic_payload, db_client):
    """Ensure a Valid Workflow can be inserted in the proper Collection."""
    created, data = db.store_workflow(bad_generic_payload, db_client)
    assert created is False
    assert "services" in data


def test_insert_workflow_failed_no_service(valid_workflow, db_client):
    """Ensure a Valid Workflow can not be inserted if the Services are not registered."""
    valid_workflow['services'] = ["IDONOTEXIST"]
    created, data = db.store_workflow(valid_workflow, db_client)
    assert created is False
    assert "message" in data
    assert "not all services exist" == data['message']

def test_insert_service(valid_service, db_client):
    """Ensure a Valid Service can be inserted in the proper Collection."""
    service = {
        **valid_service,
        **{'name': 'valid-insert'},
    }
    created, data = db.store_service(service, db_client)
    assert created is True
    assert 'service_id' in data
    database = db_client.get_default_database()
    query = {"_id": ObjectId(data['service_id'])}
    doc = database[db.MachineryCollections.SERVICE.value].find_one(query)
    assert doc['name'] == service['name']


def test_insert_service_failed(bad_generic_payload, db_client):
    """Ensure an Invalid Service can not be inserted in a Collection."""
    created, data = db.store_service(bad_generic_payload, db_client)
    assert created is False
    assert "address" in data


def test_service_lookup(valid_service, db_client):
    """Ensure service lookup returns True if services are found."""
    service = {
        **valid_service,
        **{'name': 'lookup'},
    }
    created, _ = db.store_service(service, db_client)
    assert created is True

    found = db.services_exists([service["name"]], db_client)
    assert found is True


def test_qualifier_restricted(valid_service, db_client):
    """Ensure exception is triggered on unknown qualifier."""
    with pytest.raises(ValueError):
        db.services_exists([valid_service["name"]], db_client, qualifier='unknown')
