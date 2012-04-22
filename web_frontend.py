import async_dropbox

from tornado.options import define, options
import tornado.ioloop
import tornado.web
import app_config

define('cookie_secret', default="dee")

class DropboxLoginHandler(tornado.web.RequestHandler, async_dropbox.DropboxMixin):
    @tornado.web.asynchronous
    def get(self):
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self._on_auth)
            return
        self.authorize_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Dropbox auth failed")
        self.set_secure_cookie(user['uid'], user['access_token'])

if __name__ == "__main__":
    settings = dict(
        cookie_secret=options.cookie_secret,
        dropbox_consumer_key=app_config.APP_KEY,
        dropbox_consumer_secret=app_config.APP_SECRET
        )
    application = tornado.web.Application([
        (r"/", DropboxLoginHandler),
    ], **settings)
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
