from protogen.generators.templates.template import Template, TSimple, TNewLine
from string import Template as StringTemplate

class MessagesReactor(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        self.add(TSimple("""

class MessageReactor:
    def __init__(self):
        self._reactions = {}

    def react(self, message):
        for (reaction in self._reactions[message.__class__]):
            reaction(message)

    def add_reaction(self, messageType, reaction):
        if messageType not in self._reactions:
            self._reactions[messageType] = [reaction]
        else:
            self._reactions[messageType].append(reaction)

            """))



class MessagingUtils(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        self.add(MessagesReactor(self._protocol))
    
