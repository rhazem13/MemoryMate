from services.EventEmitter.event_emitter import EventEmitter
from repositories.notificationsRepository import NotificationsRepository

class Event:
    def notify(self, sender_id, reciever_id, channel, args=None):
        self.emitter = EventEmitter.getInstance()
        repo = NotificationsRepository()
        data = self.getData(sender_id, reciever_id, args)
        repo.create(data)
        self.emit(data, args)

    def emit(self, data, args=None):
        self.emitter.emit(data, args)

    def getData(self, sender_id, reciever_id, args=None):
        raise NotImplementedError("getData function not implemented")
