from protogen.generators.templates.template import Template

class TMessageDeclaration(Template):
	def __init__(self, msg):
		self._msg = msg

	def body(self):
		code = """
class %{message_name}:
    pass
""" % {'message_name' : msg.get_name()}
		return code
		
		
