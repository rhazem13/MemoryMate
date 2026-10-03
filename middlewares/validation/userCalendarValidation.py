from marshmallow import Schema,fields,ValidationError,validates
from repositories.userRepository import UserRepository

class UserCalendarSchema(Schema):
    class Meta:
        fields = ("id","date","title","user_id","additional_info")
    date = fields.Date(required=True)
    title = fields.String(required=True)
    user_id = fields.Int(dump_only=True)
    additional_info = fields.String(required=False)

