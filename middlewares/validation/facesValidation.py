from marshmallow import Schema,fields,ValidationError,validates

class FacesSchema(Schema):
    class Meta:
        fields = ("id","type")
    type = fields.String(required=True)