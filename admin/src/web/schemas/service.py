from marshmallow import Schema, fields

class ServiceSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    title = fields.String()
    description = fields.String()
    keywords = fields.List(fields.String(), attribute="keywords_list")
    type_id = fields.Integer()
    type_name = fields.String()
    institution_id = fields.Integer()
    institution_name = fields.String()

service_schema = ServiceSchema()
services_schema = ServiceSchema(many=True)
