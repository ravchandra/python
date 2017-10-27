import argparse
import logging
import pexpect
import subprocess
import sys

import time
import pdb
#pdb.set_trace()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter1 = logging.Formatter('%(asctime)s - %(name)s -\
 %(pathname)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter1)
logger.addHandler(ch)

fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter1)
logger.addHandler(fh)

parser = argparse.ArgumentParser()
parser.add_argument("host", help="provide host name", nargs="?",
        default="localhost")
parser.add_argument("command", help="provide command")
#parser.add_argument("cmd_type", nargs='?',
#        help="provide i for interactive, n for non-interactive", default="n")
args = parser.parse_args()

cmd_list  = (
                ("myscp", ("scp a.txt root@localhost:/home/netsim/ravi/cfiles"),(u".*password:","netsim")),
                ("remove", ("rm -i cfiles/a.txt"), (u".*rm: remove.*\?", u"yes")),
                ("myscp2", ("scp a.txt root@127.0.0.1:/home/netsim/ravi/cfiles"),(u".*password:","netsim")),
             )

interactive = False
icmd = None
for i in cmd_list:
    if args.command in i[0]:
        interactive = True
        icmd = i
        break


class RemoteCommand(object):
    def __init__(self, command, host):
        self.command = command
        self.host = host

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
    def exec_cmd_interactive(self):
        logger.info("interactive")
        cur_cmd = icmd
        logger.info("Executing COMMAND {0}".format(cur_cmd[1]) +
                " - on HOST {0}".format(self.host))
        c = pexpect.spawnu(cur_cmd[1])
        c.expect(cur_cmd[2][0])
        c.sendline(cur_cmd[2][1])
        c.wait()
        c.kill(1)

    def exec_cmd_interactive_all(self):
        logger.info("interactive all")
        for cur_cmd in cmd_list:
            logger.info("Executing COMMAND {0}".format(cur_cmd[1]) +
                " - on HOST {0}".format(self.host))
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
