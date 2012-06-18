from protogen.generators.basic_generator import BasicGenerator
from protogen.generators.python.templates.declarations import MessageDeclarations
from protogen.generators.python.templates.json.serialization import JsonSerialization
from protogen.generators.python.templates.utils import MessagingUtils
from protogen import logger

class PythonJsonGenerator(BasicGenerator):
    def __init__(self):
        pass

    def generate(self, protocol, outdir):
        # generate declarations
        self._generate_to_file(MessageDeclarations(protocol), outdir, protocol.get_name() + "_messaging.py")
        # generate serialization
        self._generate_to_file(JsonSerialization(protocol), outdir, protocol.get_name() + "_json_messaging.py")
        # generate helper functions and utils
        self._generate_to_file(MessagingUtils(protocol), outdir, "messaging_utils.py")

