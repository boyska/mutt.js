#!/usr/bin/env python3
####
# Mutt:Just Simple
# a configuration generator for your KISS mail solution

import os
import imp
import logging
from yaml import safe_load as load
#try:
#        from yaml import CLoader as Loader, CDumper as Dumper
#except ImportError:
#        from yaml import Loader, Dumper


class PluginManager:
    def __init__(self, base_dirs):
        self.base_dirs = tuple(filter(os.path.isdir,
                               map(os.path.realpath, base_dirs)))
        self.plugin_path = {}  # name: path
        self.loaded = {}  # name: module object

        for base_dir in self.base_dirs:
            for d in os.listdir(base_dir):
                if os.path.isdir(os.path.join(base_dir, d)):
                    self.plugin_path[d] = base_dir

    def load(self, name):
        if name not in self.plugin_path:
            #TODO: our own exception
            raise ValueError('plugin %s not found in %s' %
                             (name, self.base_dirs))
        found = imp.find_module(name, [self.plugin_path[name]])
        self.loaded[name] = imp.load_module(name, *found)
        return self.loaded[name]

#TODO: s/modules/generators
modules = PluginManager(['modules'])
hooks = PluginManager(['hooks'])


def get_config(filename):
    return load(open(filename))


def run_generators(config, rules):
    for generator in rules['generators']:
        try:
            gen = modules.load(generator)
        except ValueError:
            logging.warn(
                'You asked for generator "%s" which does not exist: skipping' %
                generator)
            continue
        if not hasattr(gen, 'init'):
            logging.warn('generator "%s" is malformed: missing init' % gen)
            logging.debug("generator fields: %s" % ','.join(dir(gen)))
            continue
        gen.init(config, rules)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        logging.fatal('Wrong number of arguments')
        sys.exit(1)

    if len(sys.argv) == 2:
        os.chdir(sys.argv[1])
    config = get_config('conf.yaml')
    rules = get_config('rules.yaml')
    if not os.path.exists('build'):
        os.mkdir('build')
    run_generators(config, rules)
