from protogen.generators.basic_generator import BasicGenerator
from protogen.generators.as3.templates.declaration import MessageDeclaration
from protogen.generators.as3.templates.json.serialization import JsonSerialization
from protogen import logger

class As3JsonGenerator(BasicGenerator):
    def __init__(self):
        pass

    def generate(self, protocol, outdir):
        # generate message declarations
        #
        pass
