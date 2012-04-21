# The class responsible for authorizing the user with dropbox.
#

from pyftpdlib import ftpserver
from dropbox import client, rest, session

import app_config

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
        sess = session.DropboxSession(app_config.APP_KEY, 
                                      app_config.APP_SECRET,
                                      app_config.ACCESS_TYPE)
        request_token = sess.obtain_request_token()
        url = sess.build_authorize_url(request_token)
        print "url:", url
        print "Please visit this website and press the 'Allow' button, then hit 'Enter' here."
        raw_input()
        access_token = sess.obtain_access_token(request_token)
        
