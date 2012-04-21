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
        self.session_table = {}

    def validate_authentication(self, username, password):
        """
        Given the username and password, return true if dropbox
        validates the authentication.
        """
        sess = session.DropboxSession(app_config.APP_KEY, 
                                      app_config.APP_SECRET,
                                      app_config.ACCESS_TYPE)
        try:
            auth_token = oauth.OAuthToken.from_string(password)
        except:
            return False
        print auth_token
        sess.set_token(auth_token.key, auth_token.secret)
        # TODO(akhilg): Make sure the token is valid before returning.
        # If we are able to authenticate, add the user.
        self.add_user(username, password, "/")
        self.add_session(username, sess)
        return True

    def get_password(self, username):
        return self.user_table[username]['password']

    def add_session(self, username, session):
        self.session_table[username] = session

    def get_session(self, username):
        return self.session_table[username]
