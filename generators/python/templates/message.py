from protogen.generators.templates.template import Template
from protogen import logger
import string

class TMessageDeclaration(Template):
    def __init__(self, msg):
        Template.__init__(self, msg.get_name())
        self._msg = msg

    def body(self):
        """generate declaration for message passed in ctor"""
        msg = self._msg
        logger.verbose("generating declaration for " + msg.get_name())
        # code template
        codeTemplate = string.Template("""
class $message_name
""" )
        for field in msg.get_fields():
            self.add(TFieldDeclaration(field))
        # substitute template
        code = codeTemplate.substitute( {'message_name' : msg.get_name()})
        return code
        
        
