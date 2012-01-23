import string

class CodeBlock:
    _blocks = {}
    _order = []
    
    def __init__(self, name, body = ""):
        self._name = name
        self._body = body

    def add_block(self, block):
        self._blocks[block.get_name()] = block
        self._order.append(block.get_name())

    def insert_after(self, name, block):
        self._blocks[block.get_name()] = block
        self._order.insert(self._order.index(name) + 1, block.get_name())

    def insert_before(self, name, block):
        self._blocks[block.get_name()] = block
        self._order.insert(self._order.index(name), block.get_name())

    def get_block(self, name):
        return self._blocks[name]

    def get_name(self):
        return self._name

    def gen_body(self):
        pass # TODO : generate body from mine body and inner blocks here

class Template:
    def __init__(self, path):
        self._path = path

    def generate(self, rootCodeBlock):
        pass
