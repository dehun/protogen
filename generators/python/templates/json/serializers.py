from protogen.generators.templates.template import Template, TSimple
from protogen.utils import indent, json_pair
import string

class TJsonFieldSerializer(Template):
    def __init__(self, field, indent):
        Template.__init__(self)
        self._field = field
        self._indent = indent

    def body(self):
        code = indent(self._indent, "data += \"" + self._field.get_var_name() + "\" : " + \
                      "\"" + "msg." + self._field.get_var_name() + "\"\n")
        return code


class TJsonFieldsSerializer(Template):
    def __init__(self, fields, indent):
        Template.__init__(self)
        self._fields = fields
        self._indent = indent

    def body(self):
        indent(self._indent, "data = ''")
        for field in self._fields:
            self.add(TJsonFieldSerializer(field, self._indent))
        self.add(TSimple(indent(self._indent, "return data")))


class TJsonMessageSerializer(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message
 
    def body(self):
        codeTemplate = """
class $serializerName:
    @staticmethod
    def serialize(msg):
        data = '"$messageName" : {'
        data += $serializerName.serialize_fields(msg)
        data += '}'
        return data

    @staticmethod
    def serialize_fields(self, msg):
        """
        self.add(TJsonFieldsSerializer(self._message.get_fields(), 2))
        return string.Template(codeTemplate).substitute({'serializerName' : self._message.get_name() + "Serializer",\
                                        'messageName' : self._message.get_name()})


class TJsonSerializers(Template):
    def __init__(self, messages):
        Template.__init__(self)
        self._messages = messages

    def body(self):
        for msg in self._messages.as_list():
            self.add(TJsonMessageSerializer(msg))
