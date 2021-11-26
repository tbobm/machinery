"""Common structures for the Workflow Machinery."""
import datetime
from marshmallow import Schema, fields, EXCLUDE

class DataSchema(Schema):
    """Define Inputs and Outputs."""
    type = fields.Str()
    description = fields.Str()
    name = fields.Str()

class ServiceSchema(Schema):
    """Define a Service Entity."""
    name = fields.Str()
    address = fields.Url()
    created_at = fields.DateTime(dump_only=True, missing=datetime.datetime.utcnow())
    inputs = fields.List(fields.Nested(DataSchema))
    outputs = fields.List(fields.Nested(DataSchema))

class WorkflowSchema(Schema):
    """Define a Workflow Entity."""
    name = fields.Str()
    services = fields.List(fields.Str())
    created_at = fields.DateTime(dump_only=True, missing=datetime.datetime.utcnow())
    inputs = fields.List(fields.Nested(DataSchema))
    outputs = fields.List(fields.Nested(DataSchema))

    class Meta:  # pylint: disable=too-few-public-methods,missing-class-docstring
        unknown = EXCLUDE
