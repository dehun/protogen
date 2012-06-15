from protogen.generators.templates.template import Template
from protogen.generators.python.templates.json.serializers import TJsonSerializers
from protogen.utils import indent
from protogen import logger

class TSerializerDictInit(Template):
    def __init__(self, message, indent):
        Template.__init__(self)
        self._message = message
        self._indent = indent

    def body(self):
        messageName = self._message.get_name()
        code = indent(self._indent, "self._serializers['" + messageName + "'] = " + messageName + "Serializer\n")
        return code

class TSerializers(Template):
    def __init__(self, messages, format):
        Template.__init__(self)
        self._messages = messages
        self._format = format
        self._templates = {'json' : TJsonSerializers}

    def body(self):
        code = """
class MessageSerializer:
    def serialize(self, msg):
        serializer = self.get_serializer(msg)
        return serializer.serialize(msg)

    def get_serializer(msg):
        return self._serializers[msg.get_name()]

    def __init__(self):
        self._serializers = {}
"""
        # init dict for getting serializers by name
        logger.trace("initializing dictionary with serializers")
        for msg in self._messages.as_list():
            self.add(TSerializerDictInit(msg, 2))

        # form serializer classes
        self.add(self._templates[self._format](self._messages))

        return code
        
