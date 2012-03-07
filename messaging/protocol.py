from protogen.messaging.messages import Messages

class Protocol:
    def __init__(self, mod):
        self._messages = Messages(mod)

    def get_messages(self):
        return self._messages
