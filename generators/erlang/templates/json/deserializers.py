from protogen import logger
from protogen.generators.templates.template import Template, TSimple, TComaSeparated
from protogen.messaging.types import pgString, pgInteger, pgFloat, pgMessage, pgList, UnknownTypeException
from string import Template as StringTemplate

class MessageDeserializers(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        Template.body(self)
        for message in self._protocol.get_messages().as_list():
            logger.debug("adding template for deserializng message %s" % message.get_name())
            self.add(MessageDeserializer(message))
        self.add(TSimple('inner_deserialize_message(_UnknownMsgName, _MsgBody) -> unknown_message.'))
        self.add(TSimple("""
deserialize_message(JsonMsgBody) ->
    {struct, DecodedJson} = mochijson2:decode(JsonMsgBody),
    inner_deserialize_message(DecodedJson).
inner_deserialize_message(DecodedJson) ->
    [MessageName] = proplists:get_keys(DecodedJson),
    {struct, DecodedMsgBody} = proplists:get_value(MessageName, DecodedJson),
    inner_deserialize_message(MessageName, DecodedMsgBody).

%% helper functions
bstring_to_int(Bstring) ->
    {Int, _Rest} = string:to_integer(binary_to_list(Bstring)),
    Int.

bstring_to_float(Bstring) ->
    {Float, _Rest} = string:to_float(binary_to_list(Bstring)),
    Float.
        """))

class MessageDeserializer(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def body(self):
        # function header
        self.add(TSimple(StringTemplate('inner_deserialize_message(MsgName, MsgBody) when MsgName == "$messageName" ->').substitute({'messageName' : self._message.get_name()})))
        self.add(TSimple(StringTemplate('#$messageName{').substitute({'messageName' : self._message.get_name().lower()}), 1))
        # serialize fields
        deserializers = []
        for field in self._message.get_fields():
            deserializers.append(TFieldDeserializer(self._message, field))
        self.add(TComaSeparated(deserializers))
        # finish function
        self.add(TSimple("};", indent=1))

class TFieldDeserializer(Template):
    def __init__(self, message, field):
        Template.__init__(self)
        self._message = message
        self._field = field

    def body(self):
        self.add(TSimple(StringTemplate("$fieldName=").substitute({'fieldName' : self._field.get_var_name().lower()})))
        self.add(FieldDeserializersFactory().get_deserializer(self._message, self._field))

class FieldDeserializersFactory:
    def __init__(self):
        self._deserializers = {pgInteger : TIntegerFieldDeserializer,
                               pgFloat : TFloatFieldDeserializer,
                               pgString : TStringFieldDeserializer,
                               pgMessage : TMessageFieldDeserializer,
                               pgList : TListFieldDeserializer}

    def get_deserializer(self, message, field):
        for key in self._deserializers:
            if isinstance(field, key):
                return self._deserializers[key](field, message)
        raise UnknownTypeException()
        

class TIntegerFieldDeserializer(Template):
    def __init__(self, field, message):
        Template.__init__(self)
        self._field = field
        self._message = message

    def body(self):
        self.add(TSimple(StringTemplate("bstring_to_int(proplists:get_value($fieldName, MsgBody))").substitute({'fieldName' : self._field.get_var_name()}), indent=1))

class TFloatFieldDeserializer(Template):
    def __init__(self, field, message):
        Template.__init__(self)
        self._field = field
        self._message = message

    def body(self):
        self.add(TSimple(StringTemplate("bstring_to_float(proplists:get_value($fieldName, MsgBody))").substitute({'fieldName' : self._field.get_var_name()}), indent=1))

class TStringFieldDeserializer(Template):
    def __init__(self, field, message):
        Template.__init__(self)
        self._field = field
        self._message = message

    def body(self):
        self.add(TSimple(StringTemplate("binary_to_list(proplists:get_value($fieldName, MsgBody))").substitute({'fieldName' : self._field.get_var_name()})))

class TMessageFieldDeserializer(Template):
    def __init__(self, field, message):
        Template.__init__(self)
        self._field = field
        self._message = message

    def body(self):
        self.add(TSimple(StringTemplate("inner_deserialize_message(proplists:get_value($fieldName, MsgBody))").substitute({'fieldName' : self._field.get_var_name()})))

class TListFieldDeserializer(Template):
    def __init__(self, field, message):
        Template.__init__(self)
        self._field = field
        self._message = message

    def body(self):
        pass
