

import async_dropbox
import app_config

from tornado.options import define, options
import tornado.ioloop
import tornado.web

define('cookie_secret', default="61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=")

from random import choice
import string

def GenPassword():
    newpasswd = ""
    chars = string.letters + string.digits
    for i in range(8):
        newpasswd = newpasswd + choice(chars)
    return newpasswd

class RegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><br>Enter your dropbox userid.'
                   ' We will redirect you to dropbox for'
                   ' authentication and generate a password to connect to'
                   ' the FTP server. REMEMBER: enter the email address'
                   ' you used to register with dropbox. '
                   '<br><br><form action="/register" method="post">'
                   'Dropbox UserId: <input type="text" name="name">'
                   '<input type="submit" value="Enter">'
                   '</form></body></html>')

    def post(self):
        print self.request
        username = self.get_argument("name")
        # Replace @ with '?'
        username = username.replace('@', '?')
        self.set_secure_cookie("user", username)
        self.redirect("/authlogin")

class PasswordHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><br>NOTE: Replace "@" with "?" in your username when'
                   ' connecting to FTP server.'
                   ' <br><br><br>UserId: %s'
                   ' <br><br>Password: %s</body></html>' % 
                   (self.get_secure_cookie("user"),
                    self.get_secure_cookie("pwd")))

class FailedRegisterHandler(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><br>Failed to register.'
                   ' Please make sure you register the same email'
                   ' id you registered with dropbox. Click '
                   '<a href="/register">here</a> to try again.'
                   '</body></html>')

class DropboxAuthenticationHandler(tornado.web.RequestHandler,
                                   async_dropbox.DropboxMixin):
    @tornado.web.asynchronous
    def get(self):
        print self.request
        # If we have already generated an authorized token, get the
        # access token and create the user.
        if self.get_argument("oauth_token", None):
            self.get_authenticated_user(self._on_auth)
            return
        self.authorize_redirect(callback_uri="/authlogin")

    def _on_auth(self, user):
        print "In _on_auth_: ", self.request
        if not user:
            raise tornado.web.HTTPError(500, "Dropbox auth failed")
        username = self.get_secure_cookie("user")
        dropbox_id =  self.settings['ftp_authorizer'].get_email(
            user['access_token']['key'],
            user['access_token']['secret'])
        dropbox_id = dropbox_id.replace('@', '?')
        if (dropbox_id != username):
            self.redirect("/failedregister")
            return
        # Generate a password that can be used by the user, store it
        # in the authorizer database and give it to the user.
        password = GenPassword()
        self.set_secure_cookie("pwd", password)
        # Check with existing users to see if we already have the
        # user. If yes, remove the user before adding this new entry.
        #
        # Since we verify the email address supplied by the user with
        # what dropbox has, we ensure you can only change passwords
        # after dropbox has authenticated your identity.
        if (self.settings['ftp_authorizer'].has_user(username)):
            self.settings['ftp_authorizer'].remove_user(username)
        print "Saving ", username, " with ", password
        self.settings['ftp_authorizer'].save_user(
            username,
            password,
            user['uid'],
            user['access_token']['key'],
            user['access_token']['secret'])
        # Redirect the user to a page saying "You are ready to use ftp server."
        self.redirect("/passwd")

def web_frontend_start(authorizer):
    """
    """
    # Set up the HTTP server to redirect users to authenticate via
    # dropbox.
    settings = dict(
        cookie_secret=options.cookie_secret,
        dropbox_consumer_key=app_config.APP_KEY,
        dropbox_consumer_secret=app_config.APP_SECRET,
        ftp_authorizer=authorizer
        )

    application = tornado.web.Application([
        (r"/authlogin", DropboxAuthenticationHandler),
        (r"/failedregister", FailedRegisterHandler),
        (r"/register", RegisterHandler),
        (r"/", RegisterHandler),
        (r"/passwd", PasswordHandler),
    ], **settings)
    application.listen(app_config.HTTP_SERVER_PORT)
    tornado.ioloop.IOLoop.instance().start()

