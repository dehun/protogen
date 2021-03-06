from protogen.messaging.types import *

protocolName = "simpleMessages"

class EmptyOne(pgMessage):
    pass

class SimpleOne(pgMessage):
    title = pgString()
    body  = pgString()
    int1  = pgInteger()
    f1    = pgFloat()
    
    
class SimpleTwo(pgMessage):
    title = pgString()

class S3(pgMessage):
    title = pgString()
    ids = pgList(pgString())

class S4(pgMessage):
    title = pgString()
    ids = pgList(pgList(pgInteger()))
    
