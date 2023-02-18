from models.UserContacts.userContactsModel import UserContacts
from repositories.repository import Repository

class ContactsRepository(Repository):
    def __init__(self):
        super().__init__(UserContacts)

    def findByUserId(user_id):
        result = UserContacts.query.filter(UserContacts.user_id == user_id).all()
        return result