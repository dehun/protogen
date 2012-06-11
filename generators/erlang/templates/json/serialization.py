from protogen.generators.templates.template import Template, TSimple
from protogen.generators.erlang.templates.json.serializers import MessageSerializers
from protogen.generators.erlang.templates.json.deserializers import MessageDeserializers

class MessagesSerialization(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        self.add(TSimple("-module(json_messaging)."))
        self.add(TSimple('-include("messaging.hrl").'))
        self.add(TSimple("-export([serialize_message/1, deserialize_message/1]).")) 
        self.add(MessageSerializers(self._protocol))
        self.add(MessageDeserializers(self._protocol))

        
