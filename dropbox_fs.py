import app_config
import dropbox
import ftpserver

class DropBoxFileSystem(ftpserver.AbstractedFS):
    """

    """
    def __init__(self, root, cmd_channel):
        sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
        self.client = dropbox.client.DropboxClient(sess)

    def rmdir(self, path):
        self.client.file_delete(path)
        
    def remove(self, path):
        self.client.file_delete(path)
