from protogen.generators.basic_generator import BasicGenerator
from protogen.generators.erlang.templates.message_declarations import MessageDeclarations
from protogen.generators.erlang.templates.json.serialization import MessagesSerialization
from protogen import logger

class ErlangJsonGenerator(BasicGenerator):
    def __init__(self):
        pass

    def generate(self, protocol, outdir):
        # generate declarations
        logger.debug("generating message declarations to messaging.hrl")
        self._generate_to_file(MessageDeclarations(protocol), outdir, protocol.get_name() + "_messaging.hrl")
        # generate serialization
        logger.debug("generating message serialization")
        self._generate_to_file(MessagesSerialization(protocol), outdir, protocol.get_name() + "_json_messaging.erl")
