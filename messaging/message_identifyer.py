from binascii import crc32


class MessageIdentifyer:
    def identify(self, msg):
        return crc32(msg.get_name())
        
messageIdentifyer = MessageIdentifyer()

def get_message_identifyer():
    return messageIdentifyer
