from types import pgType

class pgMessage(pgType):
    def Serialize(self, stream):
        raise NotImplementedError()

    @staticmethod
    def Deserialize(self, stream):
        raise NotImpelemtedError()
        
