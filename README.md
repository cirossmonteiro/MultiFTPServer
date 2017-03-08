# MultiFTPServer
A Python code that allows many FTP servers, each one for a different folder, through different doors.

Packages required: mechanize (internet browsing with Python), beautifulsoup4 (parsing HTML strings), psutil (getting list of processes), pyftpdlib (configuring FTP with Python). All of them can be installed easily by PIP.

The "login route.py" is necessary if you still need to obtain the external ip of your router quickly, in case you don't know it. It works only in Cisco routers. It hasn't been tested widely. Also it can be used to open port, set port forwarding and enabling them.

The "runFTPserver.py" is responsible for preparing each FTP server.

You need to create a file providing information about the ports and folders. Each line of the file must be in the format "port;port_passive_begin-port_passive_end;complete_path_for_folder". For example: "2121;6000-6099;/home/username/Documents".
