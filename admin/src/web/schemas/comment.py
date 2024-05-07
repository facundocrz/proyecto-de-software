from marshmallow import Schema, fields, validate, validates, ValidationError
import re


class CommentSchema(Schema):
    id = fields.Integer(dump_only=True)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    content = fields.String()
    username = fields.String()
    user_id = fields.Integer()


class CreateCommentSchema(Schema):
    text = fields.Str(required=True, validate=validate.Length(min=10, max=255))

    @validates("text")
    def validate_text(self, value):
        if value and value.strip() == "":
            raise ValidationError("Comment cannot consist only of spaces.")
        if not bool(re.match(".*[A-Za-z].*[0-9]*", value)):
            raise ValidationError("Comment must contain at least one letter.")


comment_schema = CommentSchema()
comments_schema = CommentSchema(many=True)
