import argparse
import logging
import sys

parser = argparse.ArgumentParser(description="Noninteractive and Interactive \
        command execution. Must provide all the details in cmd_list \
		in remote_commands.py for interactive commands.")

parser.add_argument("command", help="provide command. If interactive, \
should be one of commands in remote_commands.py or all which would \
execute every command in remote_commands.py one after another. e.g.\n \
python shell.py testshell1 127.0.0.1 root password \n \
python shell.py all 127.0.0.1 root password")

parser.add_argument("host", help="provide host name", nargs="?",
        default="localhost")
parser.add_argument("username", help="provide user name", nargs="?",
        default="root")
parser.add_argument("password", help="provide password", nargs="?",
        default="netsim")
parser.add_argument("timeout", help="provide timeout", nargs="?",
        default=5)
parser.add_argument("logfile", help="provide log file path", nargs="?",
        default="runshell.log")
parser.add_argument("loglevel", help="provide log level as number", nargs="?",
        default=logging.INFO)
if len(sys.argv) < 2:
    parser.print_help()
    sys.exit(1)

args = parser.parse_args()
