##
## protocol generator
## invocation examples
##     protogen.py --lang=python --format=json --output=./ [--verbose] protocol.py
##

import getopt
import sys
import string
from messaging.message_loader import MessageLoader
from generators.generator_factory import GeneratorFactory
import pprint

sys.path.append('..')

class Config:
    verbose = False
    def check_and_die(self, arg):
        pass
        
    def check_completness(self):
        
        return True

        
def usage_and_die():
    print "Usage : ..."
    exit()


def parse_params():
    conf = Config()
    optReactor = {('--lang=', '-l:') : lambda arg: setattr(conf, 'lang',arg),
                  ('--format=', '-f:') : lambda arg: setattr(conf, 'format', arg),
                  ('--verbose', '-v') : lambda arg: setattr(conf, 'verbose', True),
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
    # parse input params
    conf = parse_params()
    # create directory
    # load all the messages
    messages = MessageLoader(conf.proto).get_all()

    # get generator
    pgenerator = GeneratorFactory().get_generator(conf.lang, conf.format)

    # generate to output
    pgenerator.generate(messages, conf.output)
    

if __name__ == '__main__':
    main()

