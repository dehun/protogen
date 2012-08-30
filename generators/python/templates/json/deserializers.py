from protogen.generators.templates.template import Template, TSimple, TComaSeparated
from protogen.messaging.message_identifyer import get_message_identifyer
from protogen.messaging.types import pgString, pgInteger, pgMessage, pgFloat, pgList
from string import Template as StringTemplate
from utils import indent
from protogen.generators.erlang.utils import make_erlang_atom

class JsonMessageDeserializer(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def body(self):
        pass
        

class JsonDeserializers(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        self.add(TSimple("#deserialization"))
        self.add(TSimple("import json"))
        # message deserializers
        for msg in self._protocol.get_messages().as_list():
            self.add(JsonMessageDeserializer(msg))
        # main deserializer
        self.add(TSimple(StringTemplate("""
class JsonDeserializer:
    def __init__(self):
        self._deserializers = {}
$deserializersInit

    def deserialize(self, buffer):
        decoded = json.loads(buffer)
        return self._deserialize_json(decoded)

    def _deserialize_json(self, decoded):
        MessageName = decoded.keys()[0]
        return self._deserializers[MessageName].deserialize(decoded[MessageName])
        """).substitute({'deserializersInit' : # deserializers init
                         "\n".join([StringTemplate(
                             indent(2,
                               'self._deserializers["$messageName"] = _${messageName}Deserializer()')
                             ).substitute({'messageName' : msg.get_name()}) for msg in self._protocol.get_messages().as_list()])})))
        self.add(TSimple("jsonDeserializer = JsonDeserializer()"))


class JsonMessageDeserializer(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def body(self):
        # class and function header
        self.add(TSimple(StringTemplate("""
class _${messageName}Deserializer:
    def deserialize(self, decoded):
        return $messageName(""").substitute({'messageName' : self._message.get_name()})))
        # deserializer function body
        self.add(TComaSeparated([TSimple(
            StringTemplate("$fieldName=$deserializer").substitute(
                {'fieldName' : field.get_var_name(),
                 'deserializer' :
                 DeserializersFactory().get_deserializer(field)(field,
                                                         StringTemplate('decoded["$fieldName"]').substitute({'fieldName' :
                                                                                                             field.get_var_name()}))}))
            for field in self._message.get_fields()]))
        #  deserialize fields of message
        self.add(TSimple(")", indent=2))


class DeserializersFactory:
    def __init__(self):
        self._deserializers = {pgString : string_deserializer,
                               pgInteger : integer_deserializer,
                               pgFloat : float_deserializer,
                               pgMessage : message_deserializer,
                               pgList : list_deserializer}

    def get_deserializer(self, field):
        return self._deserializers[field.__class__]

    
def string_deserializer(field, valueName):
    return StringTemplate(""" str($valueName) """).substitute(locals())

def integer_deserializer(field, valueName):
    return StringTemplate(""" int($valueName) """).substitute(locals())

def float_deserializer(field, valueName):
    return StringTemplate(""" float($valueName) """).substitute(locals())

def list_deserializer(field, valueName):
    elementType = field.get_element_type()
    deserializer = DeserializersFactory().get_deserializer(elementType)(elementType, "val")
    return StringTemplate(""" [$deserializer for val in $valueName]  """).substitute(locals())

def message_deserializer(field, valueName):
    return StringTemplate(""" jsonDeserializer.deserialize($valueName)""").substitute(locals())
