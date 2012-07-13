from protogen import logger
from protogen.generators.templates.template import Template, TSimple, TComaSeparated
from protogen.messaging.types import pgString, pgInteger, pgFloat, pgMessage, pgList, UnknownTypeException
from string import Template as StringTemplate
from protogen.generators.erlang.utils import make_erlang_atom

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
deserialize_int(Data) ->
    bstring_to_int(Data).

deserialize_float(Data) ->
    bstring_to_float(Data).

deserialize_string(Data) ->
    binary_to_list(Data).

deserialize_list(Fun, List) ->
    lists:map(Fun, List).

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
        self.add(TSimple(StringTemplate('inner_deserialize_message(<<"$messageName">>, MsgBody)  ->').substitute({'messageName' : self._message.get_name()})))
        self.add(TSimple(StringTemplate('#$messageName{').substitute({'messageName' : make_erlang_atom(self._message.get_name())}), 1))
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
        self.add(TSimple(StringTemplate("$fieldName=").substitute({'fieldName' : make_erlang_atom(self._field.get_var_name())})))
        self.add(FieldDeserializersFactory().get_deserializer(self._field, 'proplists:get_value(<<"%s">>, MsgBody)' % self._field.get_var_name()))

class FieldDeserializersFactory:
    def __init__(self):
        self._deserializers = {pgInteger : TIntegerFieldDeserializer,
                               pgFloat : TFloatFieldDeserializer,
                               pgString : TStringFieldDeserializer,
                               pgMessage : TMessageFieldDeserializer,
                               pgList : TListFieldDeserializer}

    def get_deserializer(self, field, valueName):
        return self._deserializers[field.__class__](field, valueName)
        
        

class TIntegerFieldDeserializer(Template):
    def __init__(self, field, valueName):
        Template.__init__(self)
        self._valueName = valueName

    def body(self):
        self.add(TSimple(StringTemplate('deserialize_int($valueName)').substitute({'valueName' : self._valueName}), indent=1))

class TFloatFieldDeserializer(Template):
    def __init__(self, field, valueName):
        Template.__init__(self)
        self._valueName = valueName

    def body(self):
        self.add(TSimple(StringTemplate('deserialize_float($valueName)').substitute({'valueName' : self._valueName}), indent=1))

class TStringFieldDeserializer(Template):
    def __init__(self, field, valueName):
        Template.__init__(self)
        self._valueName = valueName

    def body(self):
        self.add(TSimple(StringTemplate('deserialize_string($valueName)').substitute({'valueName' : self._valueName}), indent=1))

class TMessageFieldDeserializer(Template):
    def __init__(self, field, valueName):
        Template.__init__(self)
        self._valueName = valueName

    def body(self):
        self.add(TSimple(StringTemplate(" inner_deserialize_message(element(2, $valueName))").substitute({'valueName' : self._valueName}), indent=1))

class TListFieldDeserializer(Template):
    def __init__(self, field, valueName):
        Template.__init__(self)
        self._field = field
        self._valueName = valueName

    def body(self):
        self.add(TSimple("deserialize_list(fun(Val) -> "))
        self.add(FieldDeserializersFactory().get_deserializer(self._field.get_element_type(), 'Val'))
        self.add(TSimple("end, %s)" % (self._valueName)))
