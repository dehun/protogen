from protogen.generators.basic_generator import BasicGenerator
from protogen.generators.python.templates.root import Root as RootTemplate

class PythonJsonGenerator(BasicGenerator):
    def generate(self, protocol, outdir):
		root = RootTemplate(protocol, 'json')
		code = root.generate()
		print code
		return code
		



        
