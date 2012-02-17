from protogen.generators.templates.template import Template
from protogen.generators.python.templates.message import TMessageDeclaration

class Messages(Template):
	def __init__(self, messages):
		self._messages = messages

	def body(self):
		for message in self._messages:
			self.add(TMessageDeclaration(message))
		return """#messages declarations"""
		
	
