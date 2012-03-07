class BasicGenerator():
    def generate(self, protocol, outputDir):
        raise NotImplementedError()

    def get_name(self):
        return self.__class__.__name__
