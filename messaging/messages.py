from protogen import logger

class Messages:
    def __init__(self, mod):
        self._messagesList = _load_all_messages(mod)

    def _load_message(self, msg):
        instance = msg()
        logger.verbose("loaded  " + instance.get_name() + " message")
        return instance

    def _load_all_messages(self, mod):
        def is_message(msg):
            return isclass(msg) and issubclass(msg, pgMessage) and not is_native(msg)

        return [self._load_message(mod.__dict__[key]) for key in \
                       filter(lambda k:is_message(mod.__dict__[k]) , mod.__dict__.keys())]

    def as_list(self):
        return list(self._messagesList)
