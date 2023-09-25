import os
import sys
from termcolor import cprint

root = os.getcwd()
env = None
actions = []

for x in sys.argv[1:]:
    if(x.startswith('-e')):
        env = x.split('=')[1]
        continue
    actions.append(x)