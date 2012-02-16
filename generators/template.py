class Template:
	"""
	This is main template class
	It can hold child templates which generated code should be placed after body
	of this template or before it. Child classes should override body function.
	Parameters for template should be passes by __init__
	"""
	_childs_before = []
	_childs_after = []

	def add_top(self, child, order=0):
		""" add child template, code of which would be plased _BEFORE_ body() code """
		self._childs_before.insert(order, child)

	def add_bottom(self, child, order=0):
		""" adds child template, code of which would be placed _AFTER_ body() code"""
		self._childs_after.insert(order, child)

	def add(self, child):
		self.add_bottom(child)

	def generate(self):
		"""generate body code and child templates code"""
		code = ""
		# generate body code
		# provide possibility to add something to ourself during body phase
		body_code = self.body() 
		# generate before code
		for child in self._childs_before:
			code = code + child.generate()
		#push ourself code
		code = code + body_code
		# generate after code
		for child in self._childs_after:
			code = code + child.generate()
		return code

	def body(self):
		"""method to reimplement in child classes. body code generation is here"""
		return ""
