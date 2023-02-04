from flask import request, Blueprint
from flask_restful import abort
from repositories.contactsRepository import ContactsRepository
from middlewares.validation.userContactsValidation import UserContactsSchema
user_contacts_bp = Blueprint('usercontacts', __name__)
manySchema=UserContactsSchema(many=True)
singleSchema=UserContactsSchema()
contactsRepository= ContactsRepository()
@user_contacts_bp.post('')
def post():
    
    errors= singleSchema.validate(request.get_json())
    if errors:
        return errors, 422
    payload =UserContactsSchema().load(request.json)
    if('id' in payload):
        return "Id field shouldn't be entered",422
    return singleSchema.dump(contactsRepository.create(payload))

@user_contacts_bp.get('')
def get():
    result= contactsRepository.get_all()
    return manySchema.dump(result)

@user_contacts_bp.patch('/<int:id>')
def patch(id):
    errors= singleSchema.validate(request.get_json(),partial=True)
    if errors:
        return errors, 422
    payload =UserContactsSchema().load(request.get_json(),partial=True)
    result=contactsRepository.update(payload,id)
    if not result:
        return "Location Id doesn't exist",404
    return singleSchema.dump(result)

@user_contacts_bp.delete('/<int:id>')
def delete(id):
    result = contactsRepository.delete(id)
    if(result):
        return {"deleted":f"{id}"}
    abort(404)