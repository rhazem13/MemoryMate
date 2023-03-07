from marshmallow.validate import Length,OneOf,Regexp
from marshmallow import Schema, fields, validates, ValidationError
from repositories.userRepository import UserRepository
import datetime
import werkzeug
import json

user_types=['PATIENT','CAREGIVER']
#Minimum eight characters, at least one letter, one number and one special character:
pass_regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&)])[A-Za-z\d@$!%*#?&)]{8,}$"
#starts with +country code
phone_regex=r"^\+[1-9]{1}[0-9]{3,14}$"


class Usermemoryscheme(Schema):
    class Meta:
            
     fields = ("username","firstname","lastname","email","file","user_type","phone")
    username = fields.Str(required=True, validate=Length(min=3,max=60)) 
    firstname=fields.Str(required=True,validate=Length(min=3,max=60))
    lastname=fields.Str(required=True,validate=Length(min=3,max=60))
    # location = fields.Method("get_location", deserialize="load_location")
    email=fields.Email(required=True)
    password=fields.Str(required=True,validate=Regexp(pass_regex))
    file =fields.Raw(type=werkzeug.datastructures.FileStorage) 
    user_type=fields.Str(required=True,validate=OneOf(user_types))
    address=fields.Str(required=True,validate=Length(min=3))
    phone = fields.Str(validate=Regexp(phone_regex))
    date_of_birth=fields.Date(required=True)
class MemorySchema(Schema):

    id=fields.Int(dump_only=True)
    title = fields.Str(validate=Length(min=3,max=60))
    memo_body = fields.Str(validate=Length(min=3))
    thumbnail=fields.Str()
    memo_date = fields.Date()
    user_id=fields.Int()
    caregivers=fields.List(fields.Nested(Usermemoryscheme()))

    
        

   