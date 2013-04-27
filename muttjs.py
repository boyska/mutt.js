####
# Mutt:Just Simple
# a configuration generator for your KISS mail solution

from yaml import safe_load as load
try:
        from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
        from yaml import Loader, Dumper

#TODO: so ugly, change me with a plugin system when you can!
import mutt_basic

generators = {'mutt_basic': mutt_basic}

def get_config(filename):
    return load(open(filename))

#TODO: use a decent logging system
def warn(text):
    print ("[W] " + text, file=sys.stderr)

def run_generators(config, rules):
    for generator in rules['generators']: #oh, let's hope there is nothing else then mutt_basic
        if generator not in generators:
            warn('You asked for generator "%s" which does not exist: skipping' %
                    generator)
            continue
        if not hasattr(generators[generator], 'init'):
            warn('generator "%s" is malformed: missing init' % generator)
            continue
        generators[generator].init(config, rules)


if __name__ == '__main__':
    import os, sys
    if len(sys.argv) > 2:
        print >>sys.stderr, 'Wrong number of arguments'
        sys.exit(1)

    if len(sys.argv) == 2:
        os.chdir(sys.argv[1])
    config = get_config('conf.yaml')
    rules = get_config('rules.yaml')
    if not os.path.exists('build'):
        os.mkdir('build')
    run_generators(config, rules)
