
from dropbox import client, rest, session

import app_config
import ftpserver
import oauth.oauth as oauth

class DropBoxFileSystem(ftpserver.AbstractedFS):
    """

    """
    def __init__(self, root, cmd_channel):
        ftpserver.AbstractedFS.__init__(self, root, cmd_channel)
        # Now, check to see if the drop box access token we have is
        # still validor not.
        sess = session.DropboxSession(app_config.APP_KEY, 
                                      app_config.APP_SECRET,
                                      app_config.ACCESS_TYPE)
        access_token = self.cmd_channel.authorizer.get_access_token(
            cmd_channel.username)
        if access_token is None:
            return False
        sess.set_token(access_token['key'], access_token['secret'])
        self.client = client.DropboxClient(sess)


    def validpath(self, path):
        return True

    def rmdir(self, path):
        try:
            print path
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

    def isdir(self, path):
        return not self.isfile(path)

    # Get the list of files in the directory.
    def listdir(self, path):
        try:
            print "LIST " , path
            dir_listing = self.get_metadata(path)['contents']
            return dir_listing
        except rest.ErrorResponse, e:
            print e
            return []

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

