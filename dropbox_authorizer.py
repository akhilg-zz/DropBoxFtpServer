# The class responsible for authorizing the user with dropbox.
#

from pyftpdlib import ftpserver
from dropbox import client, rest, session

import app_config
import oauth.oauth as oauth


class DropBoxAuthorizer(ftpserver.DummyAuthorizer):
    """
    """
    def __init__(self):
        """
        Initialize the session.
        """
        ftpserver.DummyAuthorizer.__init__(self)

    def validate_authentication(self, username, password):
        """
        Given the username and password, return true if dropbox
        validates the authentication.
        """
        sess = session.DropboxSession(app_config.APP_KEY, 
                                      app_config.APP_SECRET,
                                      app_config.ACCESS_TYPE)
        auth_token = oauth.OAuthToken('', '')
        try:
            auth_token.from_string(password)
        except:
            return False
        # If we are able to authenticate, add the user.
        self.add_user(username, password, "/")
        return True
