from protogen.generators.template import Template

class Root(Template):
	def __init__(self, messages):
		self._messages = messages

	def body(self):
		return """ root body """
		
		
