import app_config
from dropbox import client, rest, session
import ftpserver

class DropBoxFileSystem(ftpserver.AbstractedFS):
    """

    """
    def __init__(self, root, cmd_channel):
        sess = session.DropboxSession(app_config.APP_KEY,
                                      app_config.APP_SECRET,
                                      app_config.ACCESS_TYPE)
        self.client = client.DropboxClient(sess)
        ftpserver.AbstractedFS.__init__(self, root, cmd_channel)
        print self._cwd

    def rmdir(self, path):
        self.client.file_delete(path)
        
    def remove(self, path):
        self.client.file_delete(path)
        
