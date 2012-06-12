from protogen import logger
import pprint

class Template:
    """
    This is main template class
    It can hold child templates which generated code should be placed after body
    of this template or before it. Child classes should override body function.
    Parameters for template should be passes by __init__
    """
    def __init__(self, additional_name = None):
        # set name of template
        self._name = self.__class__.__name__
        if (additional_name):
            self._name += "/" + additional_name
        # initialize arrays
        self._childs_before = []
        self._childs_after  = []


    def get_name(self):
        return self._name

    def add_top(self, child, order=0):
        """ add child template, code of which would be plased _BEFORE_ body() code """
        self._childs_before.insert(order, child)

    def add_bottom(self, child, order=0):
        """ adds child template, code of which would be placed _AFTER_ body() code"""
        self._childs_after.insert(order, child)

    def add(self, child):
        self._childs_after.append(child)

    def generate(self):
        """generate body code and child templates code"""
        code = ""
        # generate body code
        logger.debug("generating body of " + self.get_name())
        body_code = self.body()
        # generate before code
        for child in self._childs_before:
            code = code + child.generate()
        #push ourself code
        if body_code:
            code = code + body_code
        # generate after code
        for child in self._childs_after:
            code = code + child.generate()
        return code

    def body(self):
        logger.debug("in body of " + self.get_name())
        """method to reimplement in child classes. body code generation is here"""
        return ""
 

class TSimple(Template):
    def __init__(self, body, indent=0):
        Template.__init__(self)
        self._body = body
        self._indent=indent

    def body(self):
        return "    " * self._indent + self._body + "\n"


class TComaSeparated(Template):
    def __init__(self, templates, coma = ',', indent=0):
        Template.__init__(self)
        self._templates = templates
        self._indent = indent
        self._coma = coma

    def body(self):
        first = True
        for temp in self._templates:
            if not first:
                self.add(TSimple(self._coma, self._indent))
            first = False
            self.add(temp)
                
