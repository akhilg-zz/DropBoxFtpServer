
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

    def get_metadata(self, path):
        return self.client.metadata(path)

    def isfile(self, path):
        metadata = self.get_metadata(path)
        return not metadata['is_dir']

    # Get the list of files in the directory.
    def listdir(self, path):
        dir_listing = self.get_metadata(path)['contents']
        return dir_listing

    def compact_listdir(self, path):
        dir_listing = self.listdir(path)
        return [x['path'] for x in dir_path]

    # Put a file from dropbox
    def put_file(self, to_path, file_object):
        return self.client.put_file(to_path, file_object)

    # Get a file from dropbox.
    def get_file(self, path):
        http_response = self.client.get_file(path)
        # The FTP server treats the return value of this function as a
        # file(-like) object. So, we need to add some attributes to
        # make sure the code works.
        http_response.name = file
        http_response.closed = False
        return http_response

    def getsize(self, path):
        metadata = self.get_metadata(path)
        return metadata['bytes']

