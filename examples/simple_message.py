from protogen.messaging.message import pgMessage
from protogen.messaging.types import *

class SimpleOne(pgMessage):
    title = pgString("hello world")
    body  = pgString("hello world")
    int1  = pgNumber(10)
    f1    = pgFloat(20)
    
    
class SimpleTwo(pgMessage):
    title = pgString()
    
