import redis
from flask_socketio import SocketIO
class SocketService:
    socket = None

    @staticmethod
    def getSocket(current_app):
        if SocketService.socket is None:
            SocketService.socket = SocketIO(current_app, cors_allowed_origins='*')
        
        return SocketService.socket