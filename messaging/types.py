import sys
from inspect import isclass
from protogen import logger

class AlreadyHaveANameException(Exception):
    pass
class DontHaveANameException(Exception):
    pass

class pgType:
    def __init__(self):
        self._var_name = None

    def get_name(self):
        return self.__class__.__name__

    def get_var_name(self):
        if (not self._var_name):
            raise DontHaveANameException()
        return self._var_name

    def set_var_name(self, name):
        if (self._var_name):
            raise AlreadyHaveANameException()
        self._var_name = name

    def has_var_name(self):
        return self._var_name != None


class pgTypeWithDefault(pgType):
    def __init__(self, defaultValue):
        pgType.__init__(self)
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
    def _load_field(self, key):
        field = getattr(self, key)
        if (not field.has_var_name()):
            field.set_var_name(key)
        return field
        
    def get_fields(self):
        def is_field(field):
            return isclass(field.__class__) and issubclass(field.__class__, pgType)
        return [self._load_field(fieldkey) for fieldkey in filter(lambda k: is_field(getattr(self, k)),\
                                                self.__class__.__dict__.keys())]

def is_native(t):
    logger.debug("checking " + t.__name__ + " for nativity")
    return t.__name__ in sys.modules[__name__].__dict__
    
