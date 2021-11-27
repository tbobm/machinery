"""Storage-related unittests."""
from bson.objectid import ObjectId
from machinery import db


def test_insert_workflow(valid_workflow, db_client):
    """Ensure a Valid Workflow can be inserted in the proper Collection."""
    created, data = db.store_workflow(valid_workflow, db_client)
    assert created is True
    assert 'workflow_id' in data
    database = db_client.get_default_database()
    doc = database[db.MachineryCollections.WORKFLOW.value].find_one({"_id": ObjectId(data['workflow_id'])})
    assert doc['name'] == valid_workflow['name']


def test_insert_workflow_failed(bad_generic_payload, db_client):
    """Ensure a Valid Workflow can be inserted in the proper Collection."""
    created, data = db.store_workflow(bad_generic_payload, db_client)
    assert created is False
    assert "services" in data


def test_insert_service(valid_service, db_client):
    """Ensure a Valid Service can be inserted in the proper Collection."""
    created, data = db.store_service(valid_service, db_client)
    assert created is True
    assert 'service_id' in data
    database = db_client.get_default_database()
    doc = database[db.MachineryCollections.SERVICE.value].find_one({"_id": ObjectId(data['service_id'])})
    assert doc['name'] == valid_service['name']


def test_insert_service_failed(bad_generic_payload, db_client):
    """Ensure a Valid Service can be inserted in the proper Collection."""
    created, data = db.store_service(bad_generic_payload, db_client)
    assert created is False
    assert "address" in data
