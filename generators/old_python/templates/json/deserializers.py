from protogen.generators.templates.template import Template, TSimple
from protogen.utils import indent
import string


class TJsonDeserializers(Template):
    def __init__(self, messages):
        Template.__init__(self)
        self._messages = messages

    def body(self):
        pass
