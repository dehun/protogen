from protogen.messaging.types import *

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
    
