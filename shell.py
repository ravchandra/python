import pexpect
import subprocess
from pexpect import pxssh

from log import logger
from remote_commands import cmd_list

import arguments

args = arguments.args

# Setting command type to interactive if given command is found in cmd_list
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

    def remote(self):
        try:
            logger.info("remote")
            s = pxssh.pxssh(timeout=5)
            hostname = self.host
            username = self.username
            password = self.password
            s.login(hostname, username, password)
            if not interactive and args.command != "all":
                self.exec_remote_noninteractive(s=s)
            elif args.command != "all":
                self.exec_remote(s=s)
            else:
                self.exec_remote_all(s=s)
            s.logout()
        except pxssh.ExceptionPxssh as e:
            logger.error("ssh failed on login.")
        except pexpect.exceptions.TIMEOUT as e:
            logger.error("request timed out")
        except Exception as e:
            logger.error(str(e))

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

    def exec_remote_noninteractive(self,s):
        logger.info("remote non-interactive")
        cur_cmd = self.command
        logger.info("Executing COMMAND {0}".format(cur_cmd) +
                " - on HOST {0}".format(self.host))
        s.sendline(cur_cmd)
        s.prompt()
        logger.info(s.before)

i = RemoteCommand(command=args.command, host=args.host,  \
            username=args.username, password=args.password)
i.remote()
