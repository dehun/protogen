from protogen.generators.basic_generator import BasicGenerator
from protogen.generators.erlang.templates.message_declarations import MessageDeclarations
from protogen.generators.erlang.templates.serialization import MessagesSerialization

class ErlangBinaryGenerator(BasicGenerator):
    def generate(self, protocol, outdir):
        # generate declarations
        self._generate_to_file(MessageDeclarations(protocol), outdir, "messaging.hrl")
        # generate serialization
        self._generate_to_file(MessagesSerialization(protocol), outdir, "messaging.erl")
