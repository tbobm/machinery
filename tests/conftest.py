"""Pytest fixtures for machinery unittests."""
import os

import pymongo
import pytest


@pytest.fixture
def valid_workflow():
    """Simple valid Workflow JSON."""
    return {
        "name": "my-workflow",
        "services": ["service-1", "service-2"],
        "inputs": [
             {
                "name":"message",
                "type": "string",
                "description": "The text to process"
            }
        ],
        "outputs": [
            {
                "name": "message",
                "type": "string",
                "description": "The processed text"
            }
        ],
        "operations": { }
    }


@pytest.fixture(scope="session")
def db_client():
    """Return a valid MongoDB Client."""
    # TODO: mock the mongodb instance
    default_db_url = "mongodb://user:password@localhost:27017/machinery?authSource=admin"
    db_url = os.environ.get('MONGODB_URL', default_db_url)
    client = pymongo.MongoClient(db_url)
    return client
