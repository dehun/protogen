from protogen.generators.templates.template import Template

class DeserializeFactory(Template):
	def __init__(self, messages):
		self._messages = messages

	def body(self):
		pass
