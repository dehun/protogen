from protogen.generators.templates.template import Template, TSimple
from protogen.messaging.message_identifyer import get_message_identifyer
from protogen.messaging.types import pgString, pgInteger, pgMessage, pgFloat
from string import Template as StringTemplate
from utils import indent

class JsonMessageDeserializer(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def body(self):
        pass
        

class JsonDeserializers(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        self.add(TSimple("#deserialization"))
        self.add(TSimple("import json"))
        # message deserializers
        for msg in self._protocol.get_messages().as_list():
            self.add(JsonMessageDeserializer(msg))
        # main deserializer
        self.add(TSimple(StringTemplate("""
class JsonDeserializer:
    def __init__(self):
        self._deserializers = {}
$deserializersInit

    def deserialize(self, buffer):
        decoded = json.loads(buffer)
        return self._deserialize_json(decoded)

    def _deserialize_json(self, decoded):
        MessageName = decoded.keys()[0]
        return self._deserializers[MessageName].deserialize(decoded[MessageName])
        """).substitute({'deserializersInit' : # deserializers init
                         "\n".join([StringTemplate(
                             indent(2,
                               'self._deserializers["$messageName"] = _${messageName}Deserializer()')
                             ).substitute({'messageName' : msg.get_name()}) for msg in self._protocol.get_messages().as_list()])})))
