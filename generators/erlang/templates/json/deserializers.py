from protogen import logger
from protogen.generators.templates.template import Template#, TSimple
from protogen.messaging.types import pgString, pgInteger, pgFloat, pgMessage, pgList
from string import Template as StringTemplate

class MessageDeserializer(Template):
    def __init__(self, message):
        self._message = message

    def body(self):
        pass

class MessageDeserializers(Template):
    def __init__(self, protocol):
        Template.__init__(self)
        self._protocol = protocol

    def body(self):
        Template.body(self)
        for message in self._protocol.get_messages().as_list():
            logger.debug("adding template for deserializng message %s" % message.get_name())
            self.add(MessageDeserialize(message))
        self.add('deserialize_message(_UnknownMsgName, _MsgBody) -> unknown_message.')
