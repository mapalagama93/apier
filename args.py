import os
import argparse

parser = argparse.ArgumentParser(prog='apier')
parser.add_argument('-i', '--init', action='store_true', help='initialize folders and file structure at current directory. use -e flag to specify env files to be generated.') 
parser.add_argument('-c', '--curl', action='store_true', help='generate curl command instead of sending request.') 
parser.add_argument('-e', '--env', nargs='*', help='specify list of env to apply.') 
parser.add_argument('-f', '--file', nargs='*', help='specify list of actions to be performed.') 
argsv = parser.parse_args()
root = os.getcwd()
env = argsv.env if argsv.env != None else []
actions = argsv.file if argsv.file != None else []
is_curl = argsv.curl
is_init = argsv.init