from marshmallow import Schema, fields

class InstitutionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()
    address = fields.Str()
    location = fields.Str()
    web = fields.Str()
    keywords = fields.List(fields.Str(), attribute="keywords_list")
    availability_schedule = fields.Str(attribute="date_time")
    contact = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

institution_schema = InstitutionSchema()
institutions_schema = InstitutionSchema(many=True)