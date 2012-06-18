from protogen.generators.templates.template import Template
from protogen.generators.erlang.utils import make_erlang_atom

class MessageDeclaration(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def body(self):
        code = ""
        code +=  "-record(%s, {" % ( make_erlang_atom(self._message.get_name()))
        code += ",".join([make_erlang_atom(field.get_var_name()) for field in self._message.get_fields()])
        code += "})."
        code += "\n"
        return code

class MessageDeclarations(Template):
    def __init__(self, proto):
        Template.__init__(self)
        self._proto = proto

    def body(self):
        for message in self._proto.get_messages().as_list():
            self.add(MessageDeclaration(message))
        return "%%message declarations\n"
