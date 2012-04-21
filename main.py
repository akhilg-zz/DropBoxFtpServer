#!/usr/bin/env python

import os
import dropbox_authorizer
import ftpserver
import dropbox_fs

def main():
    # Instantiate a dummy authorizer for managing 'virtual' users
    authorizer = dropbox_authorizer.DropBoxAuthorizer()

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

    # Instantiate FTP server class and listen to 0.0.0.0:21
    address = ('', 21)
    ftpd = ftpserver.FTPServer(address, ftp_handler)

    # set a limit for connections
    ftpd.max_cons = 256
    ftpd.max_cons_per_ip = 5

    # start ftp server
    ftpd.serve_forever()

if __name__ == '__main__':
    main()
