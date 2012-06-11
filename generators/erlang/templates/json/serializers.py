from protogen import logger
from protogen.generators.templates.template import Template, TSimple
from protogen.messaging.types import pgString, pgInteger, pgFloat, pgMessage, pgList
from string import Template as StringTemplate

class MessageSerializers(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        Template.body(self)
        for message in self._protocol.get_messages().as_list():
            logger.debug("adding template for serializating %s message" % message.get_name())
            self.add(MessageSerializer(message))
        self.add(TSimple("serialize_message(Msg) -> unknown_message."))


class MessageSerializer(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def body(self):
        Template.body(self)
        message = self._message
        self.add(TSimple("serialize_message(Msg) when is_record(Msg, %s) ->" % message.get_name().lower()))
        self.add(TSimple(""" lists:concat(["{ \\"%s\\" :  {", """ % message.get_name()))
        self.add(TSimple("string:join(["))
        first = True
        #serialize fields
        for field in message.get_fields():
            if (not first):
                 self.add(TSimple(",")) 
            first = False
            # serialize field
            self.add(TSimple("""lists:concat(["\\"%s\\" :", """  % field.get_var_name()))
            self.add(FieldSerializersFactory().get_field_serializer(field, message))
            self.add(TSimple("])"))
        self.add(TSimple("""], ",") """))
        self.add(TSimple(""" , "}}" ]); """))

        
class FieldSerializersFactory:
    def __init__(self):
        self._serializers = {}
        self._serializers[pgInteger] = TIntegerFieldSerializer
        self._serializers[pgString] = TStringFieldSerializer
        self._serializers[pgFloat] = TFloatFieldSerializer
        self._serializers[pgMessage] = TMessageFieldSerializer
        self._serializers[pgList] = TListFieldSerializer

    def get_field_serializer(self, field, message):
        for key in self._serializers.keys():
            if isinstance(field, key):
                return self._serializers[key](field, message)


class TStringFieldSerializer(Template):
    def __init__(self, field, message):
        Template.__init__(self)
        self._field = field
        self._message = message

    def body(self):
        tmp = StringTemplate(""" lists:concat(["\\"", Msg#$messageName.$fieldName, "\\""]) """)
        return tmp.substitute({'messageName' : self._message.get_name().lower(),
                               'fieldName' : self._field.get_var_name().lower()})


class TIntegerFieldSerializer(Template):
    def __init__(self, field, message):
        Template.__init__(self)
        self._field = field
        self._message = message

    def body(self):
        tmp = StringTemplate(""" lists:concat(["\\"", integer_to_list(Msg#$messageName.$fieldName), "\\""]) """)
        return tmp.substitute({'messageName' : self._message.get_name().lower(),
                               'fieldName' : self._field.get_var_name().lower()})


class TFloatFieldSerializer(Template):
    def __init__(self, field, message):
        Template.__init__(self)
        self._field = field
        self._message = message

    def body(self):
        tmp = StringTemplate(""" lists:concat(["\\"", integer_to_list(Msg#$messageName.$fieldName), "\\""]) """)
        return tmp.substitute({'messageName' : self._message.get_name().lower(),
                               'fieldName' : self._field.get_var_name().lower()})

class TMessageFieldSerializer(Template):
    def __init__(self, field, message):
        Template.__init__(self)
        self._field = field
        self._message = message

    def body(self):
        tmp = StringTemplate(""" lists:concat([serialize_message(Msg#$messageName.$fieldName)]) """)
        return tmp.substitute({'messageName' : self._message.get_name().lower(),
                               'fieldName' : self._field.get_var_name().lower()})



class TListFieldSerializer(Template):
    def __init__(self, field, message):
        Template.__init__(self)
        self._field = field
        self._message = message

    def body(self):
        pass
#        tmp = StringTemplate(""" lists:concat(["\\"", integer_to_list(Msg#$messageName.$fieldName), "\\""]) """)
#        return tmp.substitute({'messageName' : self._message.get_name().lower(),
#                               'fieldName' : self._field.get_var_name().lower()})




