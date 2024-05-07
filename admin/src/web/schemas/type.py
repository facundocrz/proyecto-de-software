from marshmallow import Schema, fields

class TypeSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    name = fields.String()


type_schema = TypeSchema()
types_schema = TypeSchema(many=True)