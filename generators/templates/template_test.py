import sys
import unittest
sys.path.append("..")

from protogen.generators.templates.template import Template
from protogen import logger

class TemplateTest(unittest.TestCase):
    def runTest(self):
        tmp = Template("root")
#        tmp.add(Template("one"))
        tmp.add(Template("two"))
        tmp.generate()
