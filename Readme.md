This repository contains a small python program to take still images
from the Pi Camera module

# Run as a service

Create the service file to run automatically on startup.

```
sudo vi /etc/systemd/system/cam.service
```

Add following content

```
[Unit]
Description=CAM
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/jan/cam_rest/cam_rest.py
WorkingDirectory=/home/jan/cam_rest
Restart=always
User=jan

[Install]
WantedBy=multi-user.target
```

Next Enable and Startup this service

```
sudo systemctl enable cam
sudo systemctl start cam
```

Following are some checks and usefull system commands

```
systemctl status
systemctl list-units --state=failed

journalctl -fu cam.service

sudo systemctl daemon-reload

sudo systemctl start cam
sudo systemctl stop cam
sudo systemctl restart cam
```
