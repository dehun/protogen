from protogen.generators.templates.template import Template, TSimple
from protogen.messaging.message_identifyer import get_message_identifyer
from protogen.messaging.types import pgString, pgInteger, pgMessage, pgFloat

class MessageDeserializer(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def body(self):
        code = "\n"
        for i in range(0, len(self._message.get_fields())):
            pass
#            code += "deserialize_message(%d, MsgBin, 1, FieldNum) ->\n" % (get_message_identifyer().identify(self._message))
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
        
        
        
