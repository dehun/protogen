#from protogen import logger
from protogen.generators.templates.template import Template#, TSimple
#from protogen.messaging.types import pgString, pgInteger, pgFloat, pgMessage, pgList
#from string import Template as StringTemplate

class MessageDeserializers(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        pass
