import imp
import re
from inspect import isclass
from message import pgMessage

class MessageLoader:
    def __init__(self, path):
        self._messages_path = path

    def _load_mod(self):
        mod = imp.load_source(re.search('/(\w+?)\.py', self._messages_path).group(1), self._messages_path)
        return mod

    def _load_all_messages(self, mod):
        return filter(lambda msg: pgMessage is not msg, \
                      [mod.__dict__[key] for key in \
                       filter(lambda k: isclass(mod.__dict__[k]) and issubclass(mod.__dict__[k], pgMessage), \
                              mod.__dict__.keys())])
        
    def get_all(self):
        mod = self._load_mod()
        messages = self._load_all_messages(mod)
        del mod
        return messages

