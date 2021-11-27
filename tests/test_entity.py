from machinery import entity


def test_data_schema():
    payload = {
        "name": "message",
        "type": "string",
        "description": "short"
    }
    data_schema = entity.DataSchema()
    result = data_schema.load(payload)
    assert "name" in result.keys()
    assert "type" in result.keys()
    assert "description" in result.keys()


def test_service_schema():
    payload = {
        "name": "message",
        "address": "http://some-service.com:5000/",
        "inputs": [
            {
                "name": "message",
                "type": "string",
                "description": "short"
            }
        ],
        "outputs": [
            {
                "name": "message",
                "type": "string",
                "description": "short"
            }
        ]
    }
    service_schema = entity.ServiceSchema()
    result = service_schema.load(payload)
    assert "inputs" in result.keys() and len(result["inputs"]) == 1
    assert "outputs" in result.keys() and len(result["outputs"]) == 1


def test_workflow_schema(valid_workflow):
    workflow_schema = entity.WorkflowSchema()
    result = workflow_schema.load(valid_workflow)
    assert "inputs" in result.keys() and len(result["inputs"]) == 1
