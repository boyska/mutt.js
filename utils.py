import string
import hooks

class Template(string.Template):
    '''
    A pimped-up version of string.Template that automatically inserts
    filters (see hooks.py)
    '''
    def __init__(self, *args, **kwargs):
        string.Template.__init__(self, *args, **kwargs)
    def substitute(self, *args, **kwargs):
        kws = dict(kwargs)
        while True:
            try:
                res = super().substitute(*args, **kws)
            except KeyError as exc:
                missing = exc.args[0]
                if not missing.startswith('filter_'):
                    raise exc
                name = missing[7:]
                kws[missing] = hooks.apply_filter(name, '')
            else:
                return res
