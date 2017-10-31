import argparse
import pexpect
import subprocess
import sys
from pexpect import pxssh

import log
from remote_commands import cmd_list

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
        try:
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
                #logger.error("ERROR: {0}".format(error))
                logger.error("ssh failed on login.")
            else:
                logger.info("OUTPUT: {0}".format(result))
        except:
            logger.error("ssh failed on login.")

class Interactive(RemoteCommand):
    def remote(self):
        try:
            logger.info("remote")
            s = pxssh.pxssh()
            hostname = self.host
            username = self.username
            password = self.password
            s.login(hostname, username, password)
            if args.command != "all":
                self.exec_remote(s=s)
            else:
                self.exec_remote_all(s=s)
            s.logout()
        except Exception:
            logger.error("ssh failed on login.")

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


if not interactive and args.command != "all":
    n = NonInteractive(command=args.command, host=args.host, \
            username=args.username, password=args.password)
    n.exec_cmd()
else:
    i = Interactive(command=args.command, host=args.host,  \
            username=args.username, password=args.password)
    i.remote()
