from protogen.generators.templates.template import Template
from protogen.generators.python.templates.messages import Messages
from protogen.generators.python.templates.deserialize_factory import DeserializeFactory
from protogen.generators.python.templates.serialize import TSerializers
from protogen.generators.python.templates.deserialize import TDeserializers

class Root(Template):
    def __init__(self, protocol, format):
        Template.__init__(self)
        self._protocol = protocol
        self._format = format

    def body(self):
        self.add(Messages(self._protocol.get_messages()))
        self.add(TSerializers(self._protocol.get_messages(), self._format))
        self.add(TDeserializers(self._messages))
 
