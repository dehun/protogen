from protogen.generators.templates.template import Template, TSimple, TNewLine
from string import Template as StringTemplate

class MessageDeclaration(Template):
    def __init__(self, message):
        Template.__init__(self)
        self._message = message

    def body(self):
        self.add(TSimple(StringTemplate("class $messageName:").substitute({'messageName' : self._message.get_name()})))
        # __init__
        self.add(TSimple(StringTemplate("def __init__(self, $fields):").substitute({'fields' :
                                                                                    ",".join([field.get_var_name()
                                                                                              for field in self._message.get_fields()])}),
                         indent = 1))
        # set value of fields
        for field in self._message.get_fields():
            self.add(TSimple(StringTemplate("self.$fieldName = $fieldName").substitute({'fieldName' :
                                                                                        field.get_var_name()}),
                             indent = 2))
        self.add(TNewLine(count = 2))

class MessageDeclarations(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        self.add(TSimple("""
# message declarations
# AUTO GENERATED
# do not edit by hands
        """))
        for message in self._protocol.get_messages().as_list():
            self.add(MessageDeclaration(message))
    
