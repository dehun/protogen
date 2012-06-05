from protogen.generators.templates.template import Template, TSimple
from protogen.messaging.message_identifyer import get_message_identifyer
from protogen.messaging.types import pgString, pgNumber, pgMessage, pgFloat

class MessageDeserializer(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def _deserialize_field(self, message, field):
        pass

    def body(self):
        code = "\n"
        code += "deserialize_message(%d, MsgBin) ->\n" % (get_message_identifyer().identify(self._message))
        code += "    #%s{" % (self._message.get_name().lower())
        code += ",".join([self._deserialize_field(self._message, field) for field in self._message.get_fields()])
        code + "     };\n"
        return code


class MessageDeserializers(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        for message in self._protocol.get_messages().as_list():
            self.add(MessageDeserializer(message))
        self.add(TSimple("deserialize_message(UnknownMessageId, MsgBin) -> unknown_message.\n"))

        return """
        extract_message_id(MsgBin) ->
            <<MsgId::32>> = list_to_binary(binary_to_list(MsgBin, 1, 4)),
            MsgId.

        deserialize_message(MsgBin) ->
            deserialize_message(extract_message_id(Msg), Msg).\n
        """
        
        
        
