from protogen.messaging.messages import Messages

class Protocol:
    def __init__(self, mod):
        self._name = mod.__dict__["protocolName"]
        self._messages = Messages(mod)

    def get_messages(self):
        return self._messages

    def get_name(self):
        return self._name
