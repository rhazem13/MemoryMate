from marshmallow.validate import Length,OneOf,Regexp,URL
from marshmallow import Schema, fields, validates, ValidationError
import datetime
import werkzeug



user_types=['PATIENT','CAREGIVER']
#Minimum eight characters, at least one letter, one number and one special character:
pass_regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&)])[A-Za-z\d@$!%*#?&)]{8,}$"
#starts with +country code
phone_regex=r"^\+[1-9]{1}[0-9]{3,14}$"
channels=['sms','call','whatsapp']


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
    date_of_birth=fields.Date(required=True)
    @validates('date_of_birth')
    def is_notborn_in_future(self,value):
        """'value' is the datetime parsed from time_created by marshmasllow"""
        now = datetime.datetime.now().date()
        if value > now:
            raise ValidationError("Can't be born in the future!")

class LoginUserscheme(Schema):
     email=fields.Email(required=True)
     password=fields.Str(required=True,validate=Regexp(pass_regex))

class CreateResetPasswordEmailSendInputSchema(Schema):
    # the 'required' argument ensures the field exists
    email = fields.Email(required=True)
    channel=fields.Str(required=True,validate=OneOf(channels),error="the channel sent is not correct")

class VerifyEmailaddress(Schema):
    # the 'required' argument ensures the field exists
    email = fields.Email(required=True)
    verificationcode=fields.Int(required=True)

class ResetPasswordInputSchema(Schema):
    # the 'required' argument ensures the field exists
    password = fields.Str(required=True,validate=Regexp(pass_regex))
