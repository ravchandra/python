import argparse
import subprocess
import sys

parser = argparse.ArgumentParser()
parser.add_argument("host", help="provide host name")
parser.add_argument("command", help="provide command")
args = parser.parse_args()

class RemoteCommand(object):
    def __init__(self, host, command):
        self.host = host
        self.command = command

    def exec_cmd(self):
        print "Executing command {0}".format(self.command),
        print "on host {0}".format(self.host)
        ssh = subprocess.Popen(["ssh", "%s" % self.host, self.command],
                                          shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            print "ERROR: {0}".format(error)
        else:
            print "OUTPUT: {0}".format(result)

r = RemoteCommand(args.host , args.command)
r.exec_cmd()
