from protogen.generators.basic_generator import BasicGenerator
from protogen.generators.python.templates.root import Root

class PythonJsonGenerator(BasicGenerator):
    def generate(self, messages, outdir):
		root = Root(messages)
		code = root.generate()
		print code
		return code
		



        
