"""Pytest fixtures for machinery unittests."""
import os

import pymongo
import pytest
from machinery.api import create_app
from examples.services.upper import create_upper


@pytest.fixture
def client():
    app = create_app()

    with app.test_client() as client:
        yield client


@pytest.fixture
def valid_workflow():
    """Simple valid Workflow JSON."""
    return {
        "name": "my-workflow",
        "services": ["some-service", "some-service"],
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


@pytest.fixture
def valid_service():
    """Simple valid Service JSON."""
    return {
        "name": "some-service",
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


@pytest.fixture
def bad_generic_payload():
    """Return an Invalid Payload."""
    return {
        "name": "invalid",
        "ok": False
    }

@pytest.fixture(scope="session")
def db_client():
    """Return a valid MongoDB Client."""
    # TODO: mock the mongodb instance
    default_db_url = "mongodb://user:password@localhost:27017/machinery?authSource=admin"
    db_url = os.environ.get('MONGO_URI', default_db_url)
    client = pymongo.MongoClient(db_url)
    return client


@pytest.fixture
def upper_client():
    upper = create_upper()
    with upper.test_client() as upper_client:
        yield upper_client


@pytest.fixture
def valid_upper():
    """Return a valid string to transform"""
    return {
        "message": "The Sun will raise again!"
    }