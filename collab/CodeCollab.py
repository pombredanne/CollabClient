import subprocess, re, tempfile
from getpass import getpass

class CodeCollabClient:
    def create_collab(self, title, overview):
        out = subprocess.check_output(['ccollab', '--no-browser','admin', 'review', 'create', '--title', title, '--custom-field' , 'Overview="%s"' % overview])
        review_regex = re.compile(r"Review #(\d*):")
        regex_id = review_regex.search(out).group(1)
        return regex_id

    def add_diffs(self, reviewid, diff, comment='From commit logs'):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(diff)
        f.close()
        subprocess.check_output(['ccollab', '--no-browser', 'adddiffs', '--upload-comment', comment, reviewid, f.name])

    def add_reviewers(self, reviewid, author, reviewers):
        command = ['ccollab','--no-browser','admin','review']
        if reviewers is '':
            command.append('copy-participants')
            command.append('last')
            command.append(reviewid)
        else:
            reviewlist = reviewers.split(',')
            command.append('set-participants')
            command.append(reviewid)
            command.append('--participant')
            command.append('author=%s' % author)
            for reviewer in reviewlist:
                command.append('--participant')
                command.append('reviewer=%s' % reviewer)
        subprocess.check_output(command)

    def get_current_user(self):
        command = ['ccollab', '--scm', 'none', 'info']
        data = subprocess.check_output(command)
        regex = re.compile("Connected as:.*\((.*)\)", re.MULTILINE)
        user = regex.search(data).group(1)
        return user
    
    def login(self):
        user = raw_input('Enter your Code Collab username: ')
        passwd = getpass.getpass('Enter your Code Collab password: ')
        command = ['ccollab', 'login', 'https://code-collab.soma.salesforce.com', user, passwd]
        subprocess.call(command)
    
    def done(self, reviewid):
        command = ['ccollab', 'admin', 'review', 'finish', reviewid]
        subprocess.call(command)
