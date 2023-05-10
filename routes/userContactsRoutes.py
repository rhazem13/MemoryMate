from flask import request, Blueprint
from flask_restful import abort
from repositories.contactsRepository import ContactsRepository
from repositories.userRepository import UserRepository
from middlewares.validation.userContactsValidation import UserContactsSchema
from middlewares.auth import token_required

user_contacts_bp = Blueprint('usercontacts', __name__)
manySchema = UserContactsSchema(many=True)
singleSchema = UserContactsSchema()
contactsRepository = ContactsRepository()
userRepository = UserRepository()


@user_contacts_bp.post('')
@token_required
def post():
    errors = singleSchema.validate(request.get_json())
    if errors:
        return errors, 422
    id = request.current_user.id
    caregiver = userRepository.get_by_email(request.json['email'])
    if caregiver.user_type == "PATIENT":
        return "You can add only caregivers not patyines", 400
    if request.current_user.user_type !="PATIENT":
        return "You are not a patient", 400
    contacts = contactsRepository.findByUserIdAndContactId(id, caregiver.id)
    if len(contacts) > 0:
        return "You entered this caregiver before", 409
    payload = UserContactsSchema().load(request.json)
    del payload['email']
    payload['user_id'] = id
    payload['contact_id'] = caregiver.id
    if('id' in payload):
        return "Id field shouldn't be entered", 422
    return singleSchema.dump(contactsRepository.create(payload))


@user_contacts_bp.get('/patients')
@token_required
def getPatients():
    id = request.current_user.id
    result = contactsRepository.findByContactId(id)
    print(result)
    return manySchema.dump(result)


@user_contacts_bp.get('/caregivers')
@token_required
def getCaregivers():
    id = request.current_user.id
    result = contactsRepository.findByUserId(id)

    return manySchema.dump(result)


@user_contacts_bp.patch('/<int:id>')
@token_required
def patch(id):
    errors = singleSchema.validate(request.get_json(), partial=True)
    if errors:
        return errors, 422
    payload = UserContactsSchema().load(request.get_json(), partial=True)
    result = contactsRepository.update(payload, id)
    if not result:
        return "Location Id doesn't exist", 404
    return singleSchema.dump(result)


@user_contacts_bp.delete('/<int:id>')
@token_required
def delete(id):
    result = contactsRepository.delete(id)
    if(result):
        return {"deleted": f"{id}"}
    abort(404)
