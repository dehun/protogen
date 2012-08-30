import imp
import re
from types import pgMessage, is_native
from protogen import logger
from protogen.messaging.protocol import Protocol

class ProtocolLoader:
    def _load_mod(self, path):
        mod = imp.load_source(re.search('/(\w+?)\.py', path).group(1), path)
        return mod

    def load_protocol(self, path):
        mod = self._load_mod(path)
        try:
            return Protocol(mod)
        finally:
            del mod
        

