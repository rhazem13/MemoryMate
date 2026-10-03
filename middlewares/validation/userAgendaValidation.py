from marshmallow import Schema,fields,ValidationError,validates
from marshmallow.validate import Length
from repositories.userRepository import UserRepository

class UserAgendaSchema(Schema):
    class Meta:
        fields = ("id","title","start_time","user_id","repeat_interval")
    title = fields.Str(required=True,validate=Length(1, 254))
    start_time = fields.DateTime(required=True)
    user_id = fields.Int(dump_only=True)
    repeat_interval = fields.TimeDelta(required=True)
