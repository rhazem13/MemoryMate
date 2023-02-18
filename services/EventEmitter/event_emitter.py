class EventEmitter:
    emitter = None

    @staticmethod
    def getInstance():
        if not EventEmitter.emitter:
            EventEmitter.emitter = EventEmitter()
            EventEmitter.emitter._callbacks: Dict[str, callable] = {}
        return EventEmitter.emitter
    def on(self, event_name, function):
        self._callbacks[event_name] = self._callbacks.get(event_name, []) + [function]
        return function

    def emit(self, event_name, *args, **kwargs):
        [function(*args, **kwargs) for function in self._callbacks.get(event_name, [])]

    def off(self, event_name, function):
        self._callbacks.get(event_name, []).remove(function)