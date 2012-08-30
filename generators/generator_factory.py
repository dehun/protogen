from python.python_json_generator import PythonJsonGenerator
from erlang.erlang_binary_generator import ErlangBinaryGenerator
from erlang.erlang_json_generator import ErlangJsonGenerator
#from protogen.generators.as3.as3_json_generator import As3JsonGenerator

class PythonBinaryGenerator:
	pass

class CppJsonGenerator:
	pass

class CppBinaryGenerator:
	pass

class AS3BinaryGenerator:
	pass
    
class GeneratorFactory:
    def __init__(self):
        self.register_generators()
    
    def register_generators(self):
        self._generators_registered = {'python' : {'json' : PythonJsonGenerator(),
                                                   'binary' : PythonBinaryGenerator()},
                                       'c++' : {'json' : CppJsonGenerator(),
                                                'binary' : CppBinaryGenerator()},
 #                                      'as3' : {'json' : As3JsonGenerator(),
#                                                'binary' : AS3BinaryGenerator()},
                                       'erlang' : {'binary' : ErlangBinaryGenerator(),
                                                   'json' : ErlangJsonGenerator()}
                                       }
        
    def get_generator(self, lang, format):
        return self._generators_registered[lang][format]
