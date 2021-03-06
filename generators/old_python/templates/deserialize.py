from protogen.generators.templates.template import Template
from protogen.generators.python.templates.json.deserializers import TJsonDeserializers
from protogen.utils import indent


class TDeserializers(Template):
    def __init__(self, messages, format):
        Template.__init__(self)
        self._messages = messages
        self._format = format
        self._templates = {'json' : TJsonDeserializers}

    def body(self):
        code = """
class MessageDeserializer:
    def deserialize(data):
        deserializer = MessageDeserializer.get_deserializer(data)
        return deserializer.deserialize(data)

    def get_deserializer(data):
        typeName = MessageDeserializer._extract_type_name(data)
        deserializer = self._deserializers[typeName]
        return deserializer.deserialize(data)

    def __init__(self):
        self._deserializers = {}
"""
        # form dictionary of deserializers
        for msg in self._messages.as_list():
            messageName = self._message.get_name()
            code += indent(self._indent, "self._deserializers['" + messageName + "] = " + messageName + "Deserializer\n")

        # form deserializers
        self.add(self._templates[self._format](self._messages))
        
        return code
