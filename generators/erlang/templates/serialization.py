from protogen.generators.templates.template import Template, TSimple
from protogen.generators.erlang.templates.serializers import MessageSerializers
from protogen.generators.erlang.templates.deserializers import MessageDeserializers

class MessagesSerialization(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        code = ""
        code += "-module(messaging).\n"
        code += "-export([serialize_message/1, deserialize_message/1]).\n"
        self.add(MessageSerializers(self._protocol))
        self.add(MessageDeserializers(self._protocol))
        return code
