from models.UserContacts.userContactsModel import UserContacts
from repositories.repository import Repository

class ContactsRepository(Repository):
    def __init__(self):
        super().__init__(UserContacts)