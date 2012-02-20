class pgType:
    def get_name(self):
        return self.__class__.__name__


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
        
