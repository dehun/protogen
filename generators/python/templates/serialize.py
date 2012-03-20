from protogen.generators.templates.template import Template
from protogen.generators.python.templates.json.serializers import TJsonSerializers
from protogen.utils import indent

class TSerializerDict(Template):
    def __init__(self, message, indent):
        Template.__init__(self)
        self._message = message
        self._indent = indent

    def body(self):
        messageName = self._message.get_name()
        code = indent(self._indent, "serializers['" + messageName + "'] = " + messageName + "Serializer\n")
        return code

class TGetSerializer(Template):
    def __init__(self, indent):
        Template.__init__(self)
        self._indent = indent

    def body(self):
        return indent(self._indent, "return serializers[msg.get_name()]\n")

class TSerializers(Template):
    def __init__(self, messages, format):
        Template.__init__(self)
        self._messages = messages
        self._format = format
        self._templates = {'json' : TJsonSerializers}

    def body(self):
        code = """
class MessageSerializer:
    @staticmethod
    def serialize(self, msg):
        serializer = self.get_serializer(msg)
        return serializer.serialize(msg)

    @staticmethod
    def get_serializer(msg):
        serializers = {}
"""
        # form getters for serializers
        for msg in self._messages.as_list():
            self.add(TSerializerDict(msg, 2))
        self.add(TGetSerializer(2))

        # form serializer classes
        self.add(self._templates[self._format](self._messages))

        return code
        
