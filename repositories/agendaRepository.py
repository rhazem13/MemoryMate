from models.UserAgenda.userAgendaModel import UserAgenda
from repositories.repository import Repository

class AgendaRepository(Repository):
    def __init__(self):
        super().__init__(UserAgenda)