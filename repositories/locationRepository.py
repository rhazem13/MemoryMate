from models.UserLocations.userLocationsModel import UserLocationModel
from repositories.repository import Repository

class LocationRepository(Repository):
    def __init__(self):
        super().__init__(UserLocationModel)