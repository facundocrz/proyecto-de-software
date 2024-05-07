from marshmallow import Schema, fields, validate, validates, ValidationError

class RequestStatusSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()

request_status_schema = RequestStatusSchema()
request_statuses_schema = RequestStatusSchema(many=True)