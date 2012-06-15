from protogen.generators.templates.template import Template, TSimple
from protogen.generators.python.templates.json.serializers import JsonSerializers
from protogen.generators.python.templates.json.deserializers import JsonDeserializers


class JsonSerialization(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        # generate header
        self.add(TSimple("""
# serialization tools for json messaging
# auto generated
# do not edit
        """))
        # imports
        self.add(TSimple("from messaging import *"))
        # generate serializers
        self.add(JsonSerializers(self._protocol))
        # generate deserializers
        self.add(JsonDeserializers(self._protocol))
