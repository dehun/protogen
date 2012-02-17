from protogen.generators.templates.template import Template
from protogen.generators.python.templates.messages import Messages
from protogen.generators.python.templates.deserialize_factory import DeserializeFactory

class Root(Template):
	def __init__(self, messages):
		self._messages = messages

	def body(self):
		self.add(Messages(self._messages))
		self.add(DeserializeFactory(self._messages))
		
		
