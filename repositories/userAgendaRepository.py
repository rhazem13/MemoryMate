from models.UserAgenda.userAgendaModel import UserAgenda
from repositories.repository import Repository
from sqlalchemy import func
from sqlalchemy.dialects.postgresql import INTERVAL
from sqlalchemy.sql.functions import concat
from models.db import db
class UserAgendaRepository(Repository):
    def __init__(self):
        super().__init__(UserAgenda)
    
    def findWithenInterval(interval):
        result = UserAgenda.query.filter((func.date_trunc('minute',UserAgenda.start_time+UserAgenda.repeat_interval)>=func.date_trunc('minute',func.now()))&(
        func.date_trunc('minute', UserAgenda.start_time+UserAgenda.repeat_interval)<=func.date_trunc('minute',func.now()+func.cast(concat(interval, 'MINUTES'), INTERVAL)))).all()
        return result

    def updateStartTimeWithInterval():
        print('in update function ')
        UserAgenda.query.filter(UserAgenda.start_time<func.now()).update({UserAgenda.start_time:UserAgenda.start_time+UserAgenda.repeat_interval})
        db.session.commit()