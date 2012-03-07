##
## protocol generator
## invocation examples
##     protogen.py --lang=python --format=json --output=./ [--verbose] protocol.py
##

import sys
sys.path.append('..')
sys.path.append('/home/dehun/dev/home/')


import getopt

import string
from protogen.messaging.protocol_loader import ProtocolLoader
from protogen.generators.generator_factory import GeneratorFactory
from protogen import logger
import pprint


class Config:
    verbose = False
    debug = False
    def check_and_die(self, arg):
        pass
        
    def check_completness(self):
        # TODO : implement me
        return True

        
def usage_and_die():
    print "Usage : ..."
    exit()


def parse_params():
    conf = Config()
    optReactor = {('--lang=', '-l:') : lambda arg: setattr(conf, 'lang',arg),
                  ('--format=', '-f:') : lambda arg: setattr(conf, 'format', arg),
                  ('--verbose', '-v') : lambda arg: setattr(conf, 'verbose', True),
                  ('--debug', '-d') : lambda arg: setattr(conf, 'debug', True),
                  ('--output=', '-o:') : lambda arg: setattr(conf, 'output', arg),
                  ('--proto=', '-p:') : lambda arg: setattr(conf, 'proto', arg),
                  ('--help', '-h') : lambda arg: usage_and_die()}

    opts, args = getopt.getopt(sys.argv[1:], string.join([x[1][1:] for x in optReactor.keys()]).replace(' ', ''), \
                                   list([x[0][2:] for x in optReactor.keys()]))
    for opt, arg in opts:
        for keys in optReactor.keys():
            for key in keys:
                if key.find(opt) != -1:
                    optReactor[keys](arg)


    if not conf.check_completness():
        usage_and_die()

    return conf

def main():
    logger.info("starting up protogen")
    # parse input params
    conf = parse_params()
    # setup logger
    if (conf.verbose):
        logger.set_verbose(True)
    if (conf.debug):
        logger.set_debug(True)
    # create directory
    # load all the messages
    logger.info("loading protocol from path \"" + conf.proto + "\"")
    protocol = ProtocolLoader().load_protocol(conf.proto)

    # get generator
    logger.info("preparing generator")
    generator = GeneratorFactory().get_generator(conf.lang, conf.format)

    # generate to output
    logger.info("start generation")
    generator.generate(protocol, conf.output)


if __name__ == '__main__':
    main()
