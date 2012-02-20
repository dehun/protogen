import imp
import re
from inspect import isclass
from types import pgMessage, is_native
from protogen import logger

class MessageLoader:
    def __init__(self, path):
        self._messages_path = path

    def _load_mod(self):
        mod = imp.load_source(re.search('/(\w+?)\.py', self._messages_path).group(1), self._messages_path)
        return mod

    def _load_message(self, msg):
        instance = msg()
        logger.verbose("loaded  " + instance.get_name() + " message")
        return instance

    def _load_all_messages(self, mod):
        def is_message(msg):
            return isclass(msg) and issubclass(msg, pgMessage) and not is_native(msg)

        return [self._load_message(mod.__dict__[key]) for key in \
                       filter(lambda k:is_message(mod.__dict__[k]) , mod.__dict__.keys())]
        
    def get_all(self):
        mod = self._load_mod()
        messages = self._load_all_messages(mod)
        del mod
        return messages

