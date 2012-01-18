class MessageLoader:
    def __init__(self, path):
        self._messages_path = path

    def get_all(self):
        raise NotImplementedError()
