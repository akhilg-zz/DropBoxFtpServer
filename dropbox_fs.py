
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
        try:
            self.client.file_delete(path)
        except rest.ErrorResponse:
            pass

    def remove(self, path):
        try:
            self.client.file_delete(path)
        except rest.ErrorResponse :
            pass

    def get_metadata(self, path):
        return self.client.metadata(path)

    def isfile(self, path):
        try:
            metadata = self.get_metadata(path)
            return not metadata['is_dir']
        except rest.ErrorResponse:
            return None

    # Get the list of files in the directory.
    def listdir(self, path):
        try:
            dir_listing = self.get_metadata(path)['contents']
            return dir_listing
        except rest.ErrorResponse:
            return None

    def compact_listdir(self, path):
        dir_listing = self.listdir(path)
        if dir_listing is None:
            return []
        return [x['path'] for x in dir_path]

    # Put a file from dropbox
    def put_file(self, to_path, file_object):
        try:
            return self.client.put_file(to_path, file_object)
        except rest.ErrorResponse:
            return None

    # Get a file from dropbox.
    def get_file(self, path):
        """
        Returns httplib.HTTPResponse that contains the content of the
        file specified by path.
        """
        try:
            http_response = self.client.get_file(path)
            # The FTP server treats the return value of this function as a
            # file(-like) object. So, we need to add some attributes to
            # make sure the code works.
            http_response.name = path
            http_response.closed = False
            return http_response
        except rest.ErrorResponse:
            return None

    def getsize(self, path):
        """
        Returns the size of the file defined by the path.
        """
        try:
            metadata = self.get_metadata(path)
            return metadata['bytes']
        except rest.ErrorResponse:
            return 0

