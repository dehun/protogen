from python.python_json_generator import PythonJsonGenerator

class PythonBinaryGenerator:
	pass

class CppJsonGenerator:
	pass

class CppBinaryGenerator:
	pass

class AS3JsonGenerator:
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
                                       'as3' : {'json' : AS3JsonGenerator(),
                                                'binary' : AS3BinaryGenerator()}
                                       }
        
    def get_generator(self, lang, format):
        return self._generators_registered[lang][format]
