from marshmallow.validate import Length,OneOf,Regexp
from marshmallow import Schema, fields, validates, ValidationError
from repositories.userRepository import UserRepository
import datetime
import werkzeug
import json

class MemorySchema(Schema):

    id=fields.Int(dump_only=True)
    title = fields.Str(validate=Length(min=3,max=60))
    memo_body = fields.Str(validate=Length(min=3))
    thumbnail=fields.Str()
    memo_date = fields.Date()
    user_id=fields.Int()
    @validates('memo_date')
    def cant_make_memory_in_future (self,value):
        """'value' is the datetime parsed from time_created by marshmasllow"""
        now = datetime.datetime.now().date()
        if value > now:
            raise ValidationError("cant make memory in_future!")
    @validates('user_id')
    def validate_user(self,user_id):
        if not UserRepository.get_by_id(self,user_id):
            raise ValidationError ("not valid user")
        
        

   