# The class responsible for authorizing the user with dropbox.
#

from dropbox import client, rest, session

import app_config
import ftpserver
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
        # Try to get the account info to make sure the authentication
        # is correct.
        db_client = client.DropboxClient(sess)
        try:
            db_client.account_info()
        except:
            return False
        # TODO(akhilg): Each user should have his/her own home directory.
        # If we are able to authenticate, add the user.
        existing_password = self.get_password(username)
        if (existing_password is None or
            existing_password != password):
            self.remove_user(username)
            self.add_user(username, password, "/", perm="elrdfmwM",
                          dropbox_session=sess)
        return True

    def get_password(self, username):
        if username in self.user_table:
            return self.user_table[username]['password']
        return None

    def get_session(self, username):
        return self.user_table[username]['session']
