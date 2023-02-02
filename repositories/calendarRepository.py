from models.UserCalendar.userCalendarModel import UserCalendarModel
from repositories.repository import Repository

class CalendarRepository(Repository):
    def __init__(self):
        super().__init__(UserCalendarModel)