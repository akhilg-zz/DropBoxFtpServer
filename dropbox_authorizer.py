# The class responsible for authorizing the user with dropbox.
#

import os

from dropbox import client, rest, session

import app_config
import ftpserver
import oauth.oauth as oauth

def GenHomeDirectory(uid):
    """
    Generate a directory for the unique dropbox uid.
    """
    return os.path.join(app_config.HOME_DIR_ROOT, str(uid))

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
        user_password = self.get_password(username)
        if (user_password is None or password != user_password):
            return False
        # Now, check to see if the drop box access token we have is
        # still valid or not. If not, return false. The user should be
        # asked to regenerate the password
        sess = session.DropboxSession(app_config.APP_KEY, 
                                      app_config.APP_SECRET,
                                      app_config.ACCESS_TYPE)
        access_token = self.get_access_token(username)
        if access_token is None:
            print "Missing authentication token for ", username
            return False
        sess.set_token(access_token['key'], access_token['secret'])
        # Try to get the account info to make sure the authentication
        # is correct.
        db_client = client.DropboxClient(sess)
        try:
            # TODO(akhilg): Currently disabled, as it slows down the
            # authentication.
            return True
            # account_info = db_client.account_info()
        except rest.ErrorResponse, e:
            print e, " Failed to authenticate with drop box"
            return False
        return True

    def get_password(self, username):
        if username in self.user_table:
            return self.user_table[username]['pwd']
        return None

    def get_access_token(self, username):
        if username in self.user_table:
            return dict(key=self.user_table[username]['access_key'],
                        secret=self.user_table[username]['access_secret'])
        return None

    def get_email(self, access_key, access_secret):
        """
          Get email of the user who owns the access_key and access_secret
        """
        # Now, check to see if the drop box access token we have is
        # still valid or not. If not, return false. The user should be
        # asked to regenerate the password
        sess = session.DropboxSession(app_config.APP_KEY, 
                                      app_config.APP_SECRET,
                                      app_config.ACCESS_TYPE)
        sess.set_token(access_key, access_secret)
        # Try to get the account info to make sure the authentication
        # is correct.
        db_client = client.DropboxClient(sess)
        try:
            account_info = db_client.account_info()
            return account_info['email']
        except rest.ErrorResponse, e:
            print e
            return ""

    def save_user(self, username, password, uid, key,
                  secret):
        # Make sure we have a separate directory for each unique
        # dropbox user.
        homedir = GenHomeDirectory(uid)
        if not os.path.exists(homedir):
            os.mkdir(homedir)
        elif not os.path.isdir(homedir):
            os.remove(homedir)
            os.mkdir(homedir)
        self.add_user(username, password, homedir,
                      perm="elrdfmwM",
                      access_key=key, access_secret=secret)
