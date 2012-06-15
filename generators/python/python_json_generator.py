from protogen.generators.basic_generator import BasicGenerator
from protogen.generators.python.templates.declarations import MessageDeclarations
from protogen.generators.python.templates.json.serialization import JsonSerialization
from protogen import logger

class PythonJsonGenerator(BasicGenerator):
    def __init__(self):
        pass

    def generate(self, protocol, outdir):
        # generate declarations
        self._generate_to_file(MessageDeclarations(protocol), outdir, "messaging.py")
        # generate serialization
        self._generate_to_file(JsonSerialization(protocol), outdir, "json_messaging.py")

