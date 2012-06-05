class BasicGenerator():
    def generate(self, protocol, outputDir):
        raise NotImplementedError()

    def get_name(self):
        return self.__class__.__name__

    def _generate_to_file(self, generator, outdir, filename):
        code = generator.generate()
        print code
