import string
import os

def init(config, rules):
    os.mkdir('build/mutt')
    open('build/mutt/muttrc', 'w').write(
        string.Template(main_template).substitute(alternates='|'.join(
        config['general']['accounts'].keys()), maillists='', build_dir='conf')
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

source ${build_dir}/mutt/sending
source ${build_dir}/mutt/view
'''
