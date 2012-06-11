from protogen.generators.templates.template import Template

class MessageDeclaration(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def body(self):
        code = ""
        code +=  "-record(%s, {" % ( self._message.get_name().lower())
        code += ",".join([field.get_var_name().lower() for field in self._message.get_fields()])
        code += "})"
        code += "\n"
        return code

class MessageDeclarations(Template):
    def __init__(self, proto):
        Template.__init__(self)
        self._proto = proto

    def body(self):
        for message in self._proto.get_messages().as_list():
            self.add(MessageDeclaration(message))
        return "#message declarations\n"
