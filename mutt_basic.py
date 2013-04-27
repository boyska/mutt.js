import utils
import os
import hooks

def init(config, rules):
    if not os.path.exists('build/mutt'):
        os.mkdir('build/mutt')
    open('build/mutt/muttrc', 'w').write(
        utils.Template(main_template).substitute(
            alternates='|'.join(config['general']['accounts'].keys()),
            maillists='',
            build_dir='conf',
            )
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
