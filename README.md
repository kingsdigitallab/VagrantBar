# VagrantBar
A small python menubar app for managing Vagrant VMs on Mac OS

## Requirements:
* Mac OS (tested on High Sierra)
* Python 3
* rumps & apscheduler

## Installation
* `sudo pip3 install -r requirements.txt`

## Running
* `./Bar.py`

### Web Servers
This app(let) is able to automatically detect ports which have been changed due to port colissions. As long as the guest port is 80, 8000 or 8080 (configured in Vagrant.py), the correct port will be used when selecting "Open in Browser".

### Important!
This is a very early prototype. Be careful!
