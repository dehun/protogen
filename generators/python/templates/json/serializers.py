from protogen.generators.templates.template import Template, TSimple
from protogen.messaging.message_identifyer import get_message_identifyer
from protogen.messaging.types import pgString, pgInteger, pgFloat, pgMessage, pgList
from string import Template as StringTemplate
from utils import indent

class JsonSerializers(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        # generate by message serializers
        for message in self._protocol.get_messages().as_list():
            self.add(JsonMessageSerializer(message))

        # generate main serializer
        self.add(TSimple("from string import Template"))
        self.add(TSimple(StringTemplate("""
class JsonSerializer:
    def __init__(self):
        self._serializers = {}
$serializersInit
    def serialize(self, message):
        return self._serializers[message.__class__].serialize(message)
""").substitute({'serializersInit' : # serializers dict initialization
                 "\n".join([StringTemplate(
                     indent(2, "self._serializers[$messageName] = _${messageName}Serializer()")
                     ).substitute({'messageName' : msg.get_name()}) for msg in self._protocol.get_messages().as_list()])})))
        self.add(TSimple("jsonSerializer = JsonSerializer()"))



class JsonMessageSerializer(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def body(self):
        # declare serializer class
        self.add(TSimple(StringTemplate("""
class _${messageName}Serializer:
    def serialize(self, message):""").substitute({'messageName' : self._message.get_name()})))
        # serializer function body
        #  serialize fields of message
        self.add(TSimple("fields = {}", indent = 2))

        for field in self._message.get_fields():
            self.add(TSimple(StringTemplate(
                """fields["$fieldName"] = $serializer""").substitute({'fieldName' : field.get_var_name(),
                                                                      'serializer' :
                                                                      SerializersFactory().get_serializer(field)(field,
                                                                                                                 "message." + field.get_var_name())
                }), indent = 2))

        self.add(TSimple("""serializedFields = ','.join([Template('"$fieldName" : $fieldValue').substitute({'fieldName' : key,
        'fieldValue' : fields[key]}) for key in fields.keys()])""", indent=2))
        #  combine all into message
        self.add(TSimple(StringTemplate(
            """return Template('{ "$messageName" : { $$fields }}').substitute({'fields' : serializedFields})""").substitute({
                             'messageName' : self._message.get_name()}),
                         indent = 2))
        

class SerializersFactory:
    def __init__(self):
        self._serializers = { pgString : string_serializer,
                              pgInteger : integer_serializer,
                              pgFloat : float_serializer,
                              pgMessage : message_serializer,
                              pgList : list_serializer
                              }

    def get_serializer(self, field):
        return self._serializers[field.__class__]

def string_serializer(field, valueName):
    return StringTemplate(""" '"' + $valueName + '"'  """).substitute(locals())

def integer_serializer(field, valueName):
    return StringTemplate(""" '"' + str($valueName) + '"' """).substitute(locals())

def float_serializer(field, valueName):
    return StringTemplate(""" '"' + str($valueName) + '"' """).substitute(locals())

def message_serializer(field, valueName):
    return StringTemplate(""" jsonSerializer.serialize($valueName)""").substitute(locals())

def list_serializer(field, valueName):
    elementType = field.get_element_type()
    serializer = SerializersFactory().get_serializer(elementType)(elementType, "val")
    return StringTemplate(""" "[" + ",".join([$serializer for val in $valueName]) + "]" """).substitute(locals())



    
