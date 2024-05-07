from marshmallow import Schema, fields, validate, validates, ValidationError
import re
from src.web.schemas.comment import CommentSchema
from src.web.schemas.request_status_change import RequestStatusChangeSchema


class RequestSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    user_id = fields.Integer()
    current_status = fields.String()
    description = fields.String()
    comments = fields.Nested("CommentSchema", many=True)
    status_changes = fields.Nested("RequestStatusChangeSchema", many=True)
    service_id = fields.Integer()
    service = fields.Nested("ServiceSchema", only=("id", "title", "description", "type_id", "institution_id"))
    institution = fields.String()


class CreateRequestSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1, max=63))
    description = fields.Str(required=True, validate=validate.Length(min=1, max=255))
    service_id = fields.Integer(required=True)

    @validates("title")
    def validate_title(self, value):
        if value and value.strip() == "":
            raise ValidationError("Title cannot consist only of spaces.")
        if not bool(re.match("^[A-Za-z ]+$", value)):
            raise ValidationError("Title must contain only letters.")

    @validates("description")
    def validate_description(self, value):
        if value and value.strip() == "":
            raise ValidationError("Description cannot consist only of spaces.")
        if not bool(re.match(".*[A-Za-z].*[0-9]*", value)):
            raise ValidationError("Description must contain at least one letter.")


request_schema = RequestSchema()
requests_schema = RequestSchema(many=True)
