from models.Notifications.notificationsModel import NotificationsModel
from repositories.repository import Repository

class  NotificationsRepository(Repository):
    def __init__(self):
        super().__init__(NotificationsModel)