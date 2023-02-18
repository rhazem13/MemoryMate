from models.UserFaces.userfacesModel import UserfacesModel
from repositories.repository import Repository

class  UserfacesRepository(Repository):
    def __init__(self):
        super().__init__(UserfacesModel)