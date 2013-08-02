import subprocess, re, tempfile
from getpass import getpass

class CodeCollabClient:
    def __init__(self, server='https://code-collab.soma.salesforce.com'):
        self.server=server
        
    def create_collab(self, title, overview):
        out = subprocess.check_output(['ccollab', '--no-browser','admin', 'review', 'create', '--title', title, '--custom-field' , 'Overview=%s\n%s' % (title, overview)])
        review_regex = re.compile(r"Review #(\d*):")
        regex_id = review_regex.search(out).group(1)
        return regex_id

    def add_diffs(self, reviewid, diff, comment='From commit logs'):
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(diff)
        f.close()
        subprocess.call(['ccollab', '--no-browser', 'adddiffs', '--upload-comment', comment, reviewid, f.name])

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
        subprocess.call(command)

    def get_current_user(self):
        command = ['ccollab', '--scm', 'none', 'info']
        try:
            data = subprocess.check_output(command)
            regex = re.compile("Connected as:.*\((.*)\)", re.MULTILINE)
            user = regex.search(data).group(1)
        except:
            user = None
            
        return user
    
    def get_review_title(self, reviewid):
        return self.get_review_data(reviewid, xpath='//reviews/review/general/title/text()')
    
    def get_review_link(self, reviewid):
        return "%s/go?page=ReviewDisplay&reviewid=%s" % (self.server, reviewid)
    
    def get_last_review_id(self):
        return self.get_review_data('last', xpath='string(//reviews/review/@reviewId)')
    
    def get_review_status(self, reviewid):
        return self.get_review_data(reviewid, xpath='//reviews/review/general/phase/text()')
    
    def get_review_author(self, reviewid):
        return self.get_review_data(reviewid, xpath='//reviews/review/participants/participant/[role="Author"]/../login/text()')
        
    def get_review_data(self, reviewid, xpath=None):
        command = ['ccollab', 'admin', 'review-xml', reviewid]
        if xpath is not None:
            command.append('--xpath')
            command.append(filter)
        out = subprocess.check_output(command)
        return out
    
    def login(self):
        user = raw_input('Enter your Code Collab username: ')
        passwd = getpass.getpass('Enter your Code Collab password: ')
        command = ['ccollab', 'login', self.server, user, passwd]
        subprocess.call(command)
    
    def done(self, reviewid):
        command = ['ccollab', 'admin', 'review', 'finish', reviewid]
        subprocess.call(command)
