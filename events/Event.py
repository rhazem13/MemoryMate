from services.EventEmitter.event_emitter import EventEmitter
from repositories.notificationsRepository import NotificationsRepository
class Event:
    def __init__(self, channel) -> None:
        self.channel = channel
        self.emitter = EventEmitter.getInstance()
        self.repo = NotificationsRepository()
    
    def notify(self, sender_id, reciever_id, args=None):
        data = self.getData(sender_id, reciever_id, args)
        self.store(data)
        self.emit(data)

    def emit(self, data):
        self.emitter.emit(self.channel, data)

    def store(self, data):
        self.repo.create(data)
    
    def getData(self, sender_id, reciever_id, args=None):
        raise NotImplementedError("getData function not implemented")