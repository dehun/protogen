from protogen import logger
from protogen.generators.templates.template import Template, TSimple
from protogen.messaging.types import pgString, pgInteger, pgFloat, pgMessage, pgList, UnknownTypeException
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
        # helper functions
        self.add(TSimple("""
serialize_int(Val) -> lists:concat(['"', Val, '"']).
serialize_float(Val) -> lists:concat(['"', Val, '"']).
serialize_string(Val) ->lists:concat(['"', Val, '"']).
serialize_list(Fun, Value) -> lists:concat(["[", string:join(lists:map(Fun, Value), ","), "]"]).
        """))


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
            self.add(FieldSerializersFactory().get_field_serializer(field, "Msg#%s.%s" % (message.get_name().lower(), field.get_var_name().lower())))
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

    def get_field_serializer(self, field, valueName):
        return self._serializers[field.__class__](field, valueName)


class TStringFieldSerializer(Template):
    def __init__(self, field, valueName):
        Template.__init__(self)
        self._valueName = valueName

    def body(self):
        tmp = StringTemplate(""" serialize_string($valueName) """)
        return tmp.substitute({'valueName' : self._valueName})


class TIntegerFieldSerializer(Template):
    def __init__(self, field, valueName):
        Template.__init__(self)
        self._valueName = valueName

    def body(self):
        tmp = StringTemplate("""serialize_int($valueName)""")
        return tmp.substitute({'valueName' : self._valueName})



class TFloatFieldSerializer(Template):
    def __init__(self, field, valueName):
        Template.__init__(self)
        self._valueName = valueName

    def body(self):
        tmp = StringTemplate("""serialize_float($valueName) """)
        return tmp.substitute({'valueName' : self._valueName})

class TMessageFieldSerializer(Template):
    def __init__(self, field, valueName):
        Template.__init__(self)
        self._valueName = valueName

    def body(self):
        tmp = StringTemplate(""" serialize_message($valueName) """)
        return tmp.substitute({'valueName' : self._valueName})



class TListFieldSerializer(Template):
    def __init__(self, field, valueName):
        Template.__init__(self)
        self._valueName = valueName
        self._field = field

    
    def body(self):
        self.add(TSimple('serialize_list(fun (Value) ->'))
        self.add(FieldSerializersFactory().get_field_serializer(self._field.get_element_type(), 'Value'))
        self.add(TSimple(StringTemplate('end, $valueName)').substitute({'valueName' : self._valueName})))
        



