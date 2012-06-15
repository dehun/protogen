from protogen.generators.templates.template import Template, TSimple
from protogen.messaging.message_identifyer import get_message_identifyer
from protogen.messaging.types import pgString, pgInteger, pgMessage, pgFloat
from string import Template as StringTemplate
from utils import indent

class JsonDeserializers(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        pass
