import os
import sys
from termcolor import cprint

root = os.getcwd()
env = []
actions = []
is_curl = False

for x in sys.argv[1:]:
    if x.startswith('-e'):
        env = x.split('=')[1].split(',')
        continue
    if x == '-curl':
        is_curl = True
        continue
    actions.append(x)