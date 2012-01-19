import imp
from inspect import isclass
import sys
from message import pgMessage

class MessageLoader:
    def __init__(self, path):
        self._messages_path = path

    def _load_mod(self):
        mod = imp.load_source(re.search('/(\w+?)\.py', self._messages_path).group(1), self._messages_path)
        return mod

    def _load_all_messages(self, mod):
        return filter(lambda msg: pgMessage is not msg, \ # remove pgMessage itself
                      [mod.__dict__[key] for key in \ # retrive value from dict by a filtered keys to a list
                       filter(lambda k: issubclass(mod.__dict__[k], pgMessage), \ # check is msg keyed is subclass of pgMessage
                              filter(lambda k: isclass(mod.__dict__[k]), mod.__dict__.keys()))]) # filter for classes
        
    def get_all(self):
        mod = self._load_mod()
        messages = _load_all_messages(mod)
        del mod
        return messages

