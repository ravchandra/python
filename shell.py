import argparse
import pexpect
import subprocess
import sys
import time
from pexpect import pxssh
import getpass

import log

logger = log.logger

parser = argparse.ArgumentParser(description="Noninteractive and Interactive \
        command excution. Must provide all the details in cmd_list inside the \
        Non-interactive commands")

parser.add_argument("command", help="provide command")
parser.add_argument("host", help="provide host name", nargs="?",
        default="localhost")
parser.add_argument("username", help="provide user name", nargs="?",
        default="root")
parser.add_argument("password", help="provide password", nargs="?",
        default="netsim")
#parser.add_argument("cmd_type", nargs='?',
#        help="provide i for interactive, n for non-interactive", default="n")

if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()

cmd_list  = (
        #("myscp", ("scp a.txt root@localhost:/home/netsim/ravi/cfiles"),(u".*password:","netsim")),
        #       ("remove", ("rm -i cfiles/a.txt"), (u".*rm: remove.*\?", u"yes")),
        #        ("myscp2", ("scp a.txt root@127.0.0.1:/home/netsim/ravi/cfiles"),(u".*password:","netsim")),
                ("testshell1", "python testshell.py", (u"operation","add"), \
                    (u"number1","26"),(u"number2","37"),(u"(\d)+",""),(u"(\d)+","")),
                ("testshell2", "python testshell.py", (u"operation","sub"), \
                    (u"number1","56"),(u"number2","14"),(u"(\d)+",""),(u"(\d)+","")),
                ("testshell3", "python testshell.py", \
                    (u"operation","mul"),(u"number1","65"),(u"number2","75"),(u"(\d)+",""),(u"(\d)+","")),
             )

interactive = False
icmd = None
for i in cmd_list:
    if args.command in i[0]:
        interactive = True
        icmd = i
        break


class RemoteCommand(object):
    def __init__(self, command, host, username, password):
        self.command = command
        self.host = host
        self.username = username
        self.password = password

class NonInteractive(RemoteCommand):
    def exec_cmd(self):
        logger.info("non-interactive")
        logger.info("Executing COMMAND {0}".format(self.command) +
                " - on HOST {0}".format(self.host))
        ssh = subprocess.Popen(["ssh", "%s" % self.host, self.command],
                                          shell=False,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            logger.error("ERROR: {0}".format(error))
        else:
            logger.info("OUTPUT: {0}".format(result))

class Interactive(RemoteCommand):
    def exec_remote(self, s):
        logger.info("remote interactive")
        cur_cmd = icmd
        logger.info("Executing COMMAND {0}".format(cur_cmd[1]) +
                " - on HOST {0}".format(self.host))
        s.sendline(cur_cmd[1])
        for i in cur_cmd[2:]:
            s.expect(i[0])
            if i[1] != "":
                s.sendline(i[1])
            logger.info(s.before)
            logger.info(s.after)

    def exec_remote_all(self, s):
        logger.info("remote interactive all")
        for cur_cmd in cmd_list:
            logger.info("Executing COMMAND {0}".format(cur_cmd[1]) +
                    " - on HOST {0}".format(self.host))
            s.sendline(cur_cmd[1])
            for i in cur_cmd[2:]:
                s.expect(i[0])
                if i[1] != "":
                    s.sendline(i[1])
                logger.info(s.before)
                logger.info(s.after)

    def remote(self):
        try:
            logger.info("remote")
            s = pxssh.pxssh()
            hostname = self.host
            username = self.username
            password = self.password
            s.login (hostname, username, password)
            if args.command != "all":
                self.exec_remote(s=s)
            else:
                self.exec_remote_all(s=s)
            s.logout()
        except pxssh.ExceptionPxssh, e:
            print "pxssh failed on login."
            print str(e)

if not interactive and args.command != "all":
    n = NonInteractive(command=args.command, host=args.host, \
            username=args.username, password=args.password)
    n.exec_cmd()
else:
    i = Interactive(command=args.command, host=args.host,  \
            username=args.username, password=args.password)
    i.remote()
