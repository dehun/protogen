import sys
from inspect import isclass
from protogen import logger

class UnknownTypeException(Exception):
    pass


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

class pgList(pgType):
    def __init__(self, listType):
        pgType.__init__(self)
        self._listType = listType

    def get_element_type(self):
        return self._listType


class pgString(pgType):
    def __init__(self):
        pgType.__init__(self)


class pgInteger(pgType):
    def __init__(self):
        pgType.__init__(self)

class pgFloat(pgType):
    def __init__(self):
        pgType.__init__(self)
        
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
    
