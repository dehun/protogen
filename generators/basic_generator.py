from protogen import logger

class BasicGenerator:
    def generate(self, protocol, outputDir):
        raise NotImplementedError()

    def get_name(self):
        return self.__class__.__name__

    def _generate_to_file(self, generator, outdir, filename):
        path = outdir + filename
        logger.info("Writing %s generator's out to path %s" % (generator.get_name(), path))
        code = generator.generate()
        with open(path, "w+") as outFile:
            outFile.write(code)
