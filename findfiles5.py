import os
import argparse
import pdb

parser = argparse.ArgumentParser()
parser.add_argument("path", help="provide directory path to list")
args = parser.parse_args()

class FindFiles(object):
    def display_dir(self,dir_path,l=0):
        for i in os.listdir(dir_path):
            path = os.path.join(dir_path, i)
            if os.path.isdir(path):
                print("    "*l+"\033[34m{0}\033[00m".format(path))
                self.display_dir(path, l+1)
            else:
                print("    "*l + path)

t=FindFiles()
t.display_dir(args.path)
