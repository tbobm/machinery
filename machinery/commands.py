"""CLI utility to manage machinery."""
import pymongo
import pymongo.database

from machinery.api import create_app
from machinery.db import MachineryCollections


def _create_unique_name_index(collection: str, cursor: pymongo.database.Database):
    cursor[collection].create_index(
        [("name", pymongo.ASCENDING)],
        unique=True,
    )


def create_indexes(mongo_client: pymongo.MongoClient):
    """Create the required indexes for machinery."""
    cursor = mongo_client.get_default_database()
    _create_unique_name_index(MachineryCollections.WORKFLOW.value, cursor)
    _create_unique_name_index(MachineryCollections.SERVICE.value, cursor)


def setup_db():
    """Configure the MongoDB indexes (uniqueness)."""
    app = create_app()
    client = app.config['db']
    create_indexes(client.cx)


if __name__ == "__main__":
    setup_db()
