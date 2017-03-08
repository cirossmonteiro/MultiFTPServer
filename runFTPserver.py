from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from multiprocessing import Process, Pool

import os, commands as cmd, thread as th, time, sys
print sys.argv
p1, p2, p3, d = sys.argv[1:]
p1, p2, p3 = int(p1), int(p2), int(p3)
# Instantiate a dummy authorizer for managing 'virtual' users
authorizer = DummyAuthorizer()

# Define a new user having full r/w permissions and a read-only
# anonymous user
#authorizer.add_user('user', '12345', '.', perm='elradfmwM')
authorizer.add_anonymous(d)

# Instantiate FTP handler class
handler = FTPHandler
handler.authorizer = authorizer

# Define a customized banner (string returned when client connects)
handler.banner = "pyftpdlib based ftpd ready."

# Specify a masquerade address and the range of ports to use for
# passive connections.  Decomment in case you're behind a NAT.
handler.masquerade_address = cmd.getstatusoutput("curl ipinfo.io/ip")[-1].split('\n')[-1]#'189.122.119.14'
handler.passive_ports = range(p1, p2)

# Instantiate FTP server class and listen on 0.0.0.0:2121
address = ('', p3)
server = FTPServer(address, handler)

# set a limit for connections
server.max_cons = 256
server.max_cons_per_ip = 5

# start ftp server
server.serve_forever()
