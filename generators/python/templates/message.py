from protogen.generators.templates.template import Template
from protogen import logger
from protogen.generators.python.templates.fields import TFieldsDeclarations
import string

class TMessageDeclaration(Template):
    def __init__(self, msg):
        Template.__init__(self, msg.get_name())
        self._msg = msg

    def body(self):
        """generate declaration for message passed in ctor"""
        msg = self._msg
        # code template
        codeTemplate = string.Template("""
class $message_name:
""" )
        # substitute template
        code = codeTemplate.substitute({'message_name' : msg.get_name()})

        # add fields
        self.add(TFieldsDeclarations(msg.get_fields(), msg.get_name()))
        # ret
        return code
        
        
