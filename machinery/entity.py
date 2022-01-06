"""Common structures for the Workflow Machinery."""
import datetime
from marshmallow import Schema, fields, EXCLUDE

class DataSchema(Schema):
    """Define Inputs and Outputs."""
    type = fields.Str(required=True)
    description = fields.Str()
    name = fields.Str(required=True)

class ServiceSchema(Schema):
    """Define a Service Entity."""
    name = fields.Str(required=True)
    address = fields.Url(required=True)
    created_at = fields.DateTime(dump_only=True, load_default=datetime.datetime.utcnow)
    inputs = fields.List(fields.Nested(DataSchema))
    outputs = fields.List(fields.Nested(DataSchema))

class WorkflowSchema(Schema):
    """Define a Workflow Entity."""
    name = fields.Str(required=True)
    services = fields.List(fields.Str(), required=True)
    created_at = fields.DateTime(dump_only=True, load_default=datetime.datetime.utcnow)
    inputs = fields.List(fields.Nested(DataSchema))
    outputs = fields.List(fields.Nested(DataSchema))
    operations = fields.List(fields.Dict(keys=fields.Str(), values=fields.Str()))

    class Meta:  # pylint: disable=too-few-public-methods,missing-class-docstring
        unknown = EXCLUDE
