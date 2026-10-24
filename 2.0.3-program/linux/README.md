If you want to run it, you must first enter the command: chmod u+x Mcs_panel

If you don't want everything (including the server) to run as root, 
create a service and add the following to it: AmbientCapabilities=CAP_NET_BIND_SERVICE

/example

[Unit]
Description=Mcs_panel

[Service]
Type=simple
ExecStart=/usr/local/bin/Mcs_panel
User=your
AmbientCapabilities=CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target