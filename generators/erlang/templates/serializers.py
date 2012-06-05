from protogen.generators.templates.template import Template, TSimple
from protogen.messaging.message_identifyer import get_message_identifyer
from protogen.messaging.types import pgString, pgNumber, pgMessage, pgFloat

class MessageSerializer(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def _serialize_string_field(self, msg, field):
        return "list_to_binary(integer_to_list(len(Msg#%s.%s))), list_to_binary(Msg#%s.%s)" % (msg.get_name().lower(), field.get_var_name().lower(),
                                                                                               msg.get_name().lower(), field.get_var_name().lower())

    def _serialize_number_field(self, msg, field):
        return "<<Msg#%s.%s:32>>" % (msg.get_name().lower(), field.get_var_name().lower())

    def _serialize_float_field(self, msg, field):
        return "<<Msg#%s.%s:32>>" % (msg.get_name().lower(), field.get_var_name().lower())

    def _serialize_message_field(self, msg, field):
        return "serialize_message(Msg#%s.%s)" (msg.get_name().lower(), field.get_var_name().lower())

    def _serialize_field(self, msg, field):
        if isinstance(field, pgString):
            return self._serialize_string_field(msg, field)
        elif isinstance(field, pgNumber):
            return self._serialize_number_field(msg, field)
        elif isinstance(field, pgFloat):
            return self._serialize_float_field(msg, field)
        elif isinstance(field, pgMessage):
            return self._serialize_message_field(msg, field)
        else:
            raise UnknownTypeException()

    def body(self):
        code = "\n"
        code += "serialize_message(Msg) when Msg == #%s{} ->\n" % self._message.get_name().lower()
        code += "    list_to_binary([%s, " % get_message_identifyer().identify(self._message)
        code += "    \n,".join([self._serialize_field(self._message, field) for field in self._message.get_fields()])
        code += "]);\n"
        return code

class MessageSerializers(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        for message in self._protocol.get_messages().as_list():
            self.add(MessageSerializer(message))
        self.add(TSimple("serialize_message(UnknownMessage) -> {fail, unknown_message}."))
        return "serialize_message(unknown_message_stub_top) -> {fail, unknown_message};\n"
            
