from models.UserContacts.userContactsModel import UserContacts
from repositories.repository import Repository
from models.UserContacts.relationLevelEnum import ERelationLevel
from models.user.userModel import User


class ContactsRepository(Repository):
    def __init__(self):
        super().__init__(UserContacts)

    def findByUserId(self, user_id):
        result = UserContacts.query.join(User, User.id == UserContacts.contact_id).add_columns(User.photo_path ,UserContacts.id ,UserContacts.user_id,User.full_name, User.email, User.address, User.phone, UserContacts.contact_id, UserContacts.relation, UserContacts.bio).filter(
            UserContacts.user_id == user_id).all()
        return result

    def findByContactId(self, contact_id):
        result = UserContacts.query.join(User, User.id == UserContacts.user_id).add_columns(User.photo_path ,UserContacts.id, UserContacts.contact_id ,UserContacts.user_id, User.full_name, User.email, User.address, User.phone, UserContacts.user_id, UserContacts.relation).filter(
            UserContacts.contact_id == contact_id).all()
        return result
    
    def findByUserIdAndContactId(self, user_id, contact_id):
        result = UserContacts.query.filter(UserContacts.user_id == user_id, UserContacts.contact_id == contact_id).all()
        return result

    def get_patients_ids(self, id):
        # getting patients ids by caregiver id
        result = UserContacts.query.with_entities(
            UserContacts.user_id).filter(UserContacts.contact_id == id).all()
        print(result)
        return result
