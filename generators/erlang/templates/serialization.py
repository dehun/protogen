from protogen.generators.templates.template import Template, TSimple
from protogen.generators.erlang.templates.serializers import MessageSerializers
from protogen.generators.erlang.templates.deserializers import MessageDeserializers
from string import Template as StringTemplate

class MessagesSerialization(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        code = ""
        code += StringTemplate("-module(${protoname}_json_messaging).\n").substitute({'protoname' : self._protocol.get_name()})
        code += "-export([serialize_message/1, deserialize_message/1]).\n"
        self.add(MessageSerializers(self._protocol))
        self.add(MessageDeserializers(self._protocol))
        return code
