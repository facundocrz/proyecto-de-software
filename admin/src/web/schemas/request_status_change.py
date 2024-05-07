from marshmallow import Schema, fields, validate, validates, ValidationError

from src.web.schemas.request_status import RequestStatusSchema

class RequestStatusChangeSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime()
    status = fields.Nested("RequestStatusSchema")
    observation = fields.String()
    user = fields.Nested("UserSchema")

request_status_change_schema = RequestStatusChangeSchema()
request_status_changes_schema = RequestStatusChangeSchema(many=True)