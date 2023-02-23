from models.UserContacts.userContactsModel import UserContacts
from repositories.repository import Repository
from models.UserContacts.relationLevelEnum import ERelationLevel
class ContactsRepository(Repository):
    def __init__(self):
        super().__init__(UserContacts)

    def findByUserId(user_id):
        result = UserContacts.query.filter(UserContacts.user_id == user_id).all()
    
    def get_patients_ids(id):
        # getting patients ids by caregiver id
        result = UserContacts.query.with_entities(UserContacts.user_id).filter(UserContacts.relation==ERelationLevel.close)\
        .filter(UserContacts.contact_id==id).all()
        print(result)
        return result