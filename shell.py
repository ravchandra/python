import argparse
import pexpect
import subprocess
import sys

import time
import pdb
#pdb.set_trace()

parser = argparse.ArgumentParser()
parser.add_argument("host", help="provide host name", nargs="?",
        default="localhost")
parser.add_argument("command", help="provide command")
#parser.add_argument("cmd_type", nargs='?',
#        help="provide i for interactive, n for non-interactive", default="n")
args = parser.parse_args()

cmd_list  = (
                ("shellcopy", ("scp a.txt root@localhost:/home/netsim/ravi/cfiles"),(u".*password:","netsim")),
                ("remove", ("rm -i cfiles/a.txt"), (u".*rm: remove.*\?", u"yes")),
             )

interactive = False
icmd = None
for i in cmd_list:
    if args.command in i[0]:
        interactive = True
        icmd = i


class RemoteCommand(object):
    def __init__(self, command, host):
        self.command = command
        self.host = host

class NonInteractive(RemoteCommand):
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

class Interactive(RemoteCommand):
    def exec_cmd_interactive(self):
        print "interactive"
        cur_cmd = icmd
        print cur_cmd
        c = pexpect.spawnu(cur_cmd[1])
        c.expect(cur_cmd[2][0])
        c.sendline(cur_cmd[2][1])
        c.wait()
        c.kill(1)

    def exec_cmd_interactive_all(self):
        print "interactive all"
        for cur_cmd in cmd_list:
            print cur_cmd
            c = pexpect.spawnu(cur_cmd[1])
            c.expect(cur_cmd[2][0])
            c.sendline(cur_cmd[2][1])
            c.wait()
            time.sleep(10)
        c.kill(1)


if not interactive and args.command != 'all':
    n = NonInteractive(command=args.command, host=args.host)
    n.exec_cmd()
elif args.command != 'all':
    i = Interactive(command=args.command, host=args.host)
    i.exec_cmd_interactive()
else:
    i = Interactive(command=args.command, host=args.host)
    i.exec_cmd_interactive_all()
