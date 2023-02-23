from services.EventEmitter.event_emitter import EventEmitter
from repositories.notificationsRepository import NotificationsRepository
class Event:
    def __init__(self, channel) -> None:
        self.channel = channel
        self.emitter = EventEmitter.getInstance()
        self.repo = NotificationsRepository()
    
    def notify(self, sender_id, reciever_id, channel, args=None):
        emitter = EventEmitter.getInstance()
        repo = NotificationsRepository()
        data = self.getData(sender_id, reciever_id, args)
        repo.create(data)
        self.emit(channel)

    def emit(self, data):
        self.emitter.emit(self.channel, data)

    
    def getData(self, sender_id, reciever_id, args=None):
        raise NotImplementedError("getData function not implemented")