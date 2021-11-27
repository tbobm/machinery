"""Storage-related unittests."""
from machinery import db


def test_insert_workflow(valid_workflow, db_client):
    """Ensure a Valid Workflow can be inserted in the proper Collection."""
    created, data = db.store_workflow(valid_workflow, db_client)
    assert created is True
    assert 'workflow_id' in data
    database = db_client.get_default_database()
    doc = database[db.MachineryCollections.WORKFLOW.value].find_one({"_id": data['workflow_id']})
    assert doc['name'] == valid_workflow['name']
