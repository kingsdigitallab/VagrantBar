import subprocess
import sys

class Vagrant():
    SUPPORTED_PROVIDERS = ['virtualbox',]
    STATE_POWERON = 'running'
    STATE_POWEROFF = 'poweroff'
    STATE_SUSPEND = 'suspend'

    vms = None

    def __init__(self):
        self.update_vms()

    def get_vms(self):
        return self.vms.items()

    def update_vms(self):
        output = _cmd(['vagrant', 'global-status']) 
        self.vms = dict()
        if output is not None:
            lines = output.split('\n')
            for line in lines:
                line = line.split()
                if len(line) >= 3:
                    if line[2] in self.SUPPORTED_PROVIDERS:
                        self.vms[line[1]] = VM(line[0], line[1], line[2], line[3], line[4])

class VM():

    # These are mainly here for documentation
    key = None
    name = None
    provider = None
    state = None
    path = None

    WEB_PORTS = ['80', '8000', '8080']

    def __init__(self, key, name, provider, state, path):
        self.key = key
        self.name = name
        self.provider = provider
        self.state = state
        self.path = path

    def poweroff(self):
        _cmd_quiet(['vagrant', 'halt', self.key])

    def poweron(self):
        _cmd_quiet(['vagrant', 'up', self.key])

    def reset(self):
        _cmd_quiet(['vagrant', 'reload', self.key])

    def provision(self):
        _cmd_quiet(['vagrant', 'provision', self.key])

    def destroy(self):
        _cmd_quiet(['vagrant', 'destroy', '-f', self.key])

    def ssh(self):
        cmd = "tell application \"Terminal\" to do script \"vagrant ssh {}\"".format(self.key)
        _cmd_quiet(['osascript', '-e', cmd])

    def web(self):
        output = _cmd(['vagrant', 'port', self.key])
        if output is not None:
            lines = output.split('\n')
            for line in lines:
                l = line.strip().split()
                if len(l) > 4:
                    if l[0] in self.WEB_PORTS:
                        url = "http://127.0.0.1:{}".format(l[3])
                        _cmd_quiet(['open', url])
                        break



def _cmd(args):
    return subprocess.Popen(args, stdout=subprocess.PIPE).communicate()[0].decode("utf-8")

def _cmd_quiet(args):
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    proc.comminicate()


