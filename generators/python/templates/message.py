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
        codeTemplate = string.Template("""
class $message_name
    pass
""" )
        code = codeTemplate.substitute( {'message_name' : msg.get_name()})

        logger.debug("chunk of code generated for message " + msg.get_name())
        logger.debug(code)
        return code
        
        
