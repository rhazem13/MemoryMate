from marshmallow.validate import Length,OneOf,Regexp
from marshmallow import Schema, fields, validates, ValidationError
from repositories.userRepository import UserRepository
from middlewares.validation.userValidation import userscheme
import datetime
import werkzeug
import json

class MemorySchema(Schema):

    id=fields.Int(dump_only=True)
    title = fields.Str(validate=Length(min=3,max=60))
    memo_body = fields.Str(validate=Length(min=3))
    thumbnail=fields.URL()
    memo_date = fields.Date()
    user_id=fields.Int()
    caregivers=fields.List(fields.Int())
    #memories=fields.List(fields.Nested(Schema()), dump_only=True)

    
        

   