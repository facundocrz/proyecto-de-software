from marshmallow import Schema, fields

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    email = fields.String()
    username = fields.String()
    activo = fields.Boolean()
    first_name = fields.String()
    last_name = fields.String()

user_schema = UserSchema()
users_schema = UserSchema(many=True)