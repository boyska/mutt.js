import os
import utils

_cwd = os.path.dirname(__file__)
_build = 'build/offlineimap'


def init(config, rules):
    if not os.path.exists(_build):
        os.mkdir(_build)
    subst = {}
    subst['base_dir'] = os.path.expanduser('~/muttjs')
    subst['conf_dir'] = os.path.join(subst['base_dir'], 'conf')
    subst['mail_dir'] = os.path.join(subst['base_dir'], 'mail')
    subst['mail_sync_dir'] = os.path.join(subst['base_dir'], 'mail/sync')
    subst['mail_archive_dir'] = os.path.join(subst['base_dir'], 'mail/archive')

    def append_conf(basename, additional_values=None):
        if additional_values:
            values = subst.copy()
            values.update(additional_values)
        else:
            values = subst
        path = os.path.join(_cwd, basename)
        buf.write(utils.Template(open(path).read()).substitute(**values))
    with open(os.path.join(_build, 'offlineimap.conf'), 'w') as buf:
        append_conf('header.tmpl',
                    {'accounts':
                     ','.join(config['general']['accounts'].keys())
                     })
        for account_name, account_conf in config['general']['accounts'].items():
            additional = {'account_name': account_name}
            for key, value in account_conf.items():
                additional[key] = value
            append_conf('account.tmpl', additional)
        append_conf('footer.tmpl')
