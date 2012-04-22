import async_dropbox

import tornado.web

class DropboxLoginHandler(tornado.web.RequestHandler, async_dropbox.DropboxMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self._on_auth)
            return
        # TODO(akhilg): Do not hardcode the redirect URI.
        self.authorize_redirect(callback_uri="http://localhost:8888/")

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Dropbox auth failed")
        print "In authenticaton.", user
        # TODO(akhilg): Hook up the dropbox authorizer to get the secret key.

