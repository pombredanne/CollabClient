import subprocess, re, tempfile, sys
import getpass

class CodeCollabClient:
    '''
    Wraps the code code collaborator command line for programatic interaction
    with code collaborator
    '''
    def __init__(self, server='https://code-collab.soma.salesforce.com'):
        self.server=server
        user = None
        counter = 0
        while user is None and counter < 3:
            user = self.get_current_user()
            if user is None:
                self.login()
        
    def create_collab(self, title, overview):
        '''
        Creates a new code review
        '''
        out = subprocess.check_output(['ccollab', '--no-browser','admin', 'review', 'create', '--title', title, '--custom-field' , 'Overview=%s\n%s' % (title, overview)])
        review_regex = re.compile(r"Review #(\d*):")
        regex_id = review_regex.search(out).group(1)
        return regex_id

    def add_diffs(self, reviewid, diff, comment='From commit logs'):
        '''
        Uploads a diff file for a specified review
        '''
        f = tempfile.NamedTemporaryFile(delete=False)
        f.write(diff)
        f.close()
        subprocess.call(['ccollab', '--no-browser', 'adddiffs', '--upload-comment', comment, reviewid, f.name])

    def add_reviewers(self, reviewid, author, reviewers, observers=None):
        '''
        Adds participants for the review including authors, reviewers and observers.
        Reviewers and observers can be comma separated lists.
        '''
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
                
            if observers is not None:
                observerlist = observers.split(',')
                for observer in observerlist:
                    command.append('--participant')
                    command.append('observer=%s' % observer)
        subprocess.call(command)
        
    def add_comment(self, reviewid, comment):
        '''
        Adds a general comment to an existing code review
        '''
        command = ['ccollab', '--no-browser', 'admin', 'review', 'comment', 'create', reviewid, comment]
        subprocess.call(command)

    def get_current_user(self):
        '''
        Attempts to determine what the current user is for the code collab client
        '''
        command = ['ccollab', '--scm', 'none', 'info']
        try:
            data = subprocess.check_output(command)
            regex = re.compile("Connected as:.*\((.*)\)", re.MULTILINE)
            user = regex.search(data).group(1)
        except:
            user = None
            
        return user
    
    def get_review_title(self, reviewid):
        '''
        Returns the title for a specified review
        '''
        return self.get_review_data(reviewid, xpath='//reviews/review/general/title/text()')
    
    def get_review_link(self, reviewid):
        '''
        Generates a URL to link to a specific review
        '''
        return "%s/go?page=ReviewDisplay&reviewid=%s" % (self.server, reviewid)
    
    def get_last_review_id(self):
        '''
        Gets the id of the last review by the current user
        '''
        return self.get_review_data('last', xpath='string(//reviews/review/@reviewId)')
    
    def get_review_status(self, reviewid):
        '''
        Determines the status of a specified review
        '''
        return self.get_review_data(reviewid, xpath='//reviews/review/general/phase/text()')
    
    def get_review_author(self, reviewid):
        '''
        Gets the name of the author on a specified review
        '''
        return self.get_review_data(reviewid, xpath='//reviews/review/participants/participant/role[text()="Author"]/../login/text()')

    def get_review_reviewers(self, reviewid):
        '''
        Gets a list of reviewers on a specified review
        '''
        reviewers = self.get_review_data(reviewid, xpath='//reviews/review/participants/participant/role[text()="Reviewer"]/../login/text()')
        out = reviewers.split("\n")
        return out
        
    def get_review_observers(self, reviewid):
        '''
        Gets a list of observers for a specified review
        '''
        reviewers = self.get_review_data(reviewid, xpath='//reviews/review/participants/participant/role[text()="Observer"]/../login/text()')
        out = reviewers.split("\n")
        return out

    def get_review_data(self, reviewid, xpath=None):
        '''
        Gets data about a review.  Can specify an xpath query for specific values, otherwise, result is xml
        '''
        command = ['ccollab', 'admin', 'review-xml', reviewid]
        if xpath is not None:
            command.append('--xpath')
            command.append(xpath)
        out = subprocess.check_output(command)
        return out
    
    def login(self):
        '''
        Prompts the user and logs into code collaborator
        '''
        sys.stdin = open('/dev/tty')
        user = raw_input('Enter your Code Collab username: ')
        passwd = getpass.getpass('Enter your Code Collab password: ')
        command = ['ccollab', 'login', self.server, user, passwd]
        subprocess.call(command)
    
    def done(self, reviewid):
        '''
        Pushes a review to the next Phase
        '''
        command = ['ccollab', 'admin', 'review', 'finish', reviewid]
        subprocess.call(command)
