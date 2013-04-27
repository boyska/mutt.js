'''
Hook system (inspired by wordpress
https://codex.wordpress.org/Plugin_API
'''

from collections import defaultdict

_actions = defaultdict(list) #name: [callbacks]
_filters = defaultdict(list) #name: [callbacks]

def add_action(name, callback):
    _actions[name].append(callback)

def add_filter(name, callback):
    _filters[name].append(callback)

def do_action(name, args=[], kwargs={}):
    for callback in _actions[name]:
        if not callable(callback):
            continue
        callback(*args, **kwargs)

def apply_filter(name, filtering, args=[], kwargs={}):
    for callback in _filters[name]:
        if not callable(callback):
            continue
        filtering = callback(filtering, *args, **kwargs)
    return filtering


