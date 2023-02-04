from marshmallow.validate import Length, Range,OneOf,Regexp,URL
from marshmallow import Schema, fields, validates, ValidationError
import datetime
import werkzeug



user_types=['PATIENT','CAREGIVER']
 #Minimum eight characters, at least one letter, one number and one special character:
pass_regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
#starts with +country code
phone_regex=r"^\+[1-9]{1}[0-9]{3,14}$"


class CreateUserscheme(Schema):
    username = fields.Str(required=True, validate=Length(min=3,max=60))
    firstname=fields.Str(required=True,validate=Length(min=3,max=60))
    lastname=fields.Str(required=True,validate=Length(min=3,max=60))
    email=fields.Email(required=True)
    password=fields.Str(required=True,validate=Regexp(pass_regex))
    file =fields.Raw(type=werkzeug.datastructures.FileStorage) 
    user_type=fields.Str(required=True,validate=OneOf(user_types))
    address=fields.Str(required=True,validate=Length(min=3))
    phone = fields.Str(validate=Regexp(phone_regex))
    date_of_birth=fields.Date(required=True) #yyyy-mm-dd"
    @validates('created_at')
    def is_notborn_in_future(value):
        """'value' is the datetime parsed from time_created by marshmallow"""
        now = datetime.now()
        if value > now:
            raise ValidationError("Can't be born in the future!")
        # if the function doesn't raise an error, the check is considered passed
    created_at = fields.DateTime(datetime.datetime.now())
    @validates('created_at')
    def is_not_in_future(value):
        """'value' is the datetime parsed from time_created by marshmallow"""
        now = datetime.now()
        if value > now:
            raise ValidationError("Can't create users in the future!")
        # if the function doesn't raise an error, the check is considered passed

class LoginUserscheme(Schema):
     email=fields.Email(required=True)
     password=fields.Str(required=True,validate=Regexp(pass_regex))