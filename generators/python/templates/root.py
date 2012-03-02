from protogen.generators.templates.template import Template
from protogen.generators.python.templates.messages import Messages
from protogen.generators.python.templates.deserialize_factory import DeserializeFactory
from protogen.generators.python.templates.serialize import TSerializers

class Root(Template):
    def __init__(self, messages, format):
        Template.__init__(self)
        self._messages = messages
        self._format = format

    def body(self):
        self.add(Messages(self._messages))
        self.add(TSerializers(self._messages, self._format))
#       self.add(DeserializeFactory(self._messages))
 
