import sys
from protogen import logger

class pgType:
    def get_name(self):
        return self.__class__.__name__

    def is_native(self):
        return self._native

class pgTypeWithDefault(pgType):
    def __init__(self, defaultValue):
        self._defaultValue = defaultValue
    
    def get_default_value(self):
        return self._defaultValue


class pgString(pgTypeWithDefault):
    def __init__(self, defaultValue=""):
        pgTypeWithDefault.__init__(self, defaultValue)


class pgNumber(pgTypeWithDefault):
    def __init__(self, defaultValue=0, signed=True):
        pgTypeWithDefault.__init__(self, defaultValue )
        self._signed = signed

    def is_signed(self):
        return self._signed


class pgFloat(pgNumber):
    def __init__(self, defaultValue=0.0, signed=True):
        pgNumber.__init__(self, defaultValue, signed)
        
class pgMessage(pgType):
    def get_fields(self):
        def is_field(field):
            return isclass(field) and issubclass(field, pgType)
        return [field() for field in filter(lambda k: is_field(self.__dict__[k]),\
                                                [key for key in self.__dict__.keys()])]

def is_native(t):
    logger.debug("checking " + t.__name__ + " for nativity")
    return t.__name__ in sys.modules[__name__].__dict__
    
