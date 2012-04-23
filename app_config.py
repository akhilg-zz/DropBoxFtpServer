# Get your app key and secret from the Dropbox developer website
APP_KEY = '6qedtlyqcwt7izw'
APP_SECRET = 'ny4j2qfh2rpmjii'
# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'

# The file used to store FTP user and passwords.
USER_DATA_FILE = '.user_password'
HOME_DIR_ROOT = '/tmp'

# Name of the machine where server is running.
SERVER_HOSTNAME = ''
HTTP_SERVER_PORT = 8888
FTP_SERVER_PORT = 21

# Configuration that controls the scalability.
MAX_CONNECTIONS = 10000
MAX_CONNECTIONS_PER_IP = 10000
# Since the python API to put files in dropbox is synchronous and
# takes about 15-20 seconds for a 10MB file, we use a thread pool to
# make sure we don't block the IOLoop thread for too long.
MAX_UPLOAD_TO_DROPBOX = 20
