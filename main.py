#!/usr/bin/env python

import os
import sys
import threading

import app_config
import dropbox_authorizer
import dropbox_fs
import ftpserver

import web_frontend

def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    try:
        authorizer = dropbox_authorizer.DropBoxAuthorizer()
    except:
        raise

    # Define a new user having full r/w permissions and a read-only
    # anonymous user
    # authorizer.add_user('user', '12345', os.getcwd(), perm='elradfmwM')
    # authorizer.add_anonymous(os.getcwd())

    dtp_handler = ftpserver.ThrottledDTPHandler
    dtp_handler.read_limit = 30720  # 30 Kb/sec (30 * 1024)
    dtp_handler.write_limit = 30720  # 30 Kb/sec (30 * 1024)

    # Instantiate FTP handler class
    ftp_handler = ftpserver.FTPHandler
    ftp_handler.authorizer = authorizer
    # have the ftp handler use the alternative dtp handler class
    ftp_handler.dtp_handler = dtp_handler
    ftp_handler.abstracted_fs = dropbox_fs.DropBoxFileSystem

    # Define a customized banner (string returned when client connects)
    ftp_handler.banner = "pyftpdlib %s based ftpd ready." %ftpserver.__ver__
    
    # Specify a masquerade address and the range of ports to use for
    # passive connections.  Decomment in case you're behind a NAT.
    #ftp_handler.masquerade_address = '151.25.42.11'
    #ftp_handler.passive_ports = range(60000, 65535)

    # Start the web server.
    web_fe_thread = threading.Thread(target=web_frontend.web_frontend_start,
                                     args=(authorizer,))
    # Mark the thread as daemon so that program shuts it down when it is closing.
    web_fe_thread.daemon = True
    web_fe_thread.start()

    # Instantiate FTP server class
    address = ('', app_config.FTP_SERVER_PORT)
    ftpd = ftpserver.FTPServer(address, ftp_handler)

    # set a limit for connections
    ftpd.max_cons = 10000
    ftpd.max_cons_per_ip = 1000

    # start ftp server
    ftpd.serve_forever()

    sys.exit()
if __name__ == '__main__':
    main()
