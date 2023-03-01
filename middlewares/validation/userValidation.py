from marshmallow.validate import Length,OneOf,Regexp
from marshmallow import Schema, fields, validates, ValidationError
import datetime
import werkzeug
import json

user_types=['PATIENT','CAREGIVER']
#Minimum eight characters, at least one letter, one number and one special character:
pass_regex=r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&)])[A-Za-z\d@$!%*#?&)]{8,}$"
#starts with +country code
phone_regex=r"^\+[1-9]{1}[0-9]{3,14}$"
channels=['sms','call','whatsapp']

class CreateUserscheme(Schema):
    class Meta:
        fields = ("username","firstname","lastname","email","password","file","user_type","address","phone","date_of_birth")
    username = fields.Str(required=True, validate=Length(min=3,max=60)) 
    firstname=fields.Str(required=True,validate=Length(min=3,max=60))
    lastname=fields.Str(required=True,validate=Length(min=3,max=60))
    location = fields.Method("get_location", deserialize="load_location")
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
<<<<<<< HEAD
    # def get_location(self, obj):
    #     if(obj.location==None):
    #         return None
    #     return json.loads(obj.location)
    # def load_location(self, obj):
    #     return obj
=======
    def get_location(self, obj):
        if(obj.location==None):
            return None
        print(obj.location)
        return json.loads(obj.location)
    def load_location(self, obj):
        return obj
>>>>>>> 9daca5f8d62aba96d1dd97eb6183e932060e7b93
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
    email=fields.Email(required=True)
    password=fields.Str(required=True,validate=Regexp(pass_regex))
<<<<<<< HEAD


class userscheme(Schema):
    class Meta:
            
     fields = ("username","firstname","lastname","email","file","user_type","phone")
    username = fields.Str(required=True, validate=Length(min=3,max=60)) 
    firstname=fields.Str(required=True,validate=Length(min=3,max=60))
    lastname=fields.Str(required=True,validate=Length(min=3,max=60))
    location = fields.Method("get_location", deserialize="load_location")
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


=======
class Memoryscheme(Schema):
    thumbnail =fields.Str() 
>>>>>>> 9daca5f8d62aba96d1dd97eb6183e932060e7b93
