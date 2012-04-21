# The class responsible for authorizing the user with dropbox.
#

from pyftpdlib import ftpserver
from dropbox import client, rest, session

# Get your app key and secret from the Dropbox developer website
APP_KEY = '6qedtlyqcwt7izw'
APP_SECRET = 'ny4j2qfh2rpmjii'

# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'

class DropBoxAuthorizer(ftpserver.DummyAuthorizer):
    """
    """
    def __init__(self):
        """
        Initialize the session.
        """
        pass

    def validate_authentication(self, username, password):
        """
        Given the username and password, return true if dropbox
        validates the authentication.
        """
        print username
        print password
        sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        print "url:", url
        print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
        raw_input()
        access_token = sess.obtain_access_token(request_token)
        
