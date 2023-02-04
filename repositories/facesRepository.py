from models.Faces.facesModel import FacesModel
from repositories.repository import Repository

class FacesRepository(Repository):
    def __init__(self):
        super().__init__(FacesModel)