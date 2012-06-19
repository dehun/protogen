from protogen.generators.templates.template import Template, TSimple
from protogen.generators.erlang.templates.json.serializers import MessageSerializers
from protogen.generators.erlang.templates.json.deserializers import MessageDeserializers
from string import Template as StringTemplate

class MessagesSerialization(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        protocolName = self._protocol.get_name()
        self.add(TSimple(StringTemplate("-module(${protocolName}_json_messaging).").substitute(locals())))
        self.add(TSimple(StringTemplate('-include("${protocol_name}_messaging.hrl").').substitute(locals())))
        self.add(TSimple("-export([serialize_message/1, deserialize_message/1]).")) 
        self.add(MessageSerializers(self._protocol))
        self.add(MessageDeserializers(self._protocol))

        
