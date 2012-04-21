
from dropbox import client, rest, session

import app_config
import ftpserver
import oauth.oauth as oauth

class DropBoxFileSystem(ftpserver.AbstractedFS):
    """

    """
    def __init__(self, root, cmd_channel):
        ftpserver.AbstractedFS.__init__(self, root, cmd_channel)
        sess = cmd_channel.authorizer.get_session(cmd_channel.username)
        print sess.token
        self.client = client.DropboxClient(sess)

    def rmdir(self, path):
        self.client.file_delete(path)
        
    def remove(self, path):
        self.client.file_delete(path)

    # Get the list of files in the directory.
    def listdir(self, path):
        return self.client.metadata(path)['contents']
