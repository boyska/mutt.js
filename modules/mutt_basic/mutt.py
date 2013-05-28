#TODO: autodetect notmuch using mutt -Q nm_record (l'exit status!)
import utils
import os
import hooks

_cwd = os.path.dirname(__file__)
_templates = os.path.join(_cwd, 'templates')
_build = 'build/mutt'
def init(config, rules):
    if not os.path.exists('build/mutt'):
        os.mkdir('build/mutt')
    subst = {}
    subst['alternates'] = [iden['email'] for key, iden in config['general']['identities'].items()]
    subst['maillists'] = ''
    subst['build_dir'] = 'mail-conf'
    subst['alias_file'] = os.path.join(_build, 'aliases.build')
    subst['source_sidebar'] = ''
    for f in os.listdir(_templates):
        if f.startswith('.'):
            continue
        print(f)
        if f.endswith('.raw'):
            with open(os.path.join(_build, f[:-4]), 'w') as buf:
                buf.write(open(os.path.join(_templates, f)).read())
        else:
            with open(os.path.join(_build, f), 'w') as buf:
                buf.write(utils.Template(open(os.path.join(_templates, f)).read())
                        .substitute(**subst)
                    )
    return


main_template = '''
set mbox_type=Maildir

set folder="~/Mail/"
set mask="^."
set postponed="+drafts"
set record="+sent"

alternates "$alternates"

$maillists

$filter_mutt_pre_source
source ${build_dir}/mutt/sending
source ${build_dir}/mutt/view
$filter_mutt_post_source
'''
