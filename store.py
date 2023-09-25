import args
from jproperties import Properties
from pathlib import Path
import os
from termcolor import cprint

configs = Properties()
vars = Properties()

config_file_path = args.root + '/config.properties'
Path(config_file_path).touch(exist_ok=True)
config_file = open(config_file_path, 'rb')
configs.load(config_file, 'utf-8')

env_file_path = args.root + '/' + args.env + '.properties'
if(os.path.exists(env_file_path) == False):
    cprint(args.env + '.properties file does not exists.', attrs=['reverse'])
else:
    env_file = open(env_file_path, 'rb')
    configs.load(env_file, 'utf-8')

vars_file_path = args.root + '/vars.properties'
Path(vars_file_path).touch(exist_ok=True)
var_file = open(vars_file_path, 'rb')
vars.load(var_file, 'utf-8')


def getConfig(key, val=None):
    try:
        return configs[key].data
    except:
        return val

def getVar(key, val=None):
    try:
        return vars[key].data
    except:
        return val

def setVar(key, val):
    vars[key] = val
    with open(vars_file_path, 'wb') as f:
        vars.store(f, encoding='utf-8')

def populate(str):
    for x in vars:
        str = str.replace('{{v::' + x + '}}', getVar(x, ''))
        str = str.replace('{{var::' + x + '}}', getVar(x, ''))
        str = str.replace('{{vars::' + x + '}}', getVar(x, ''))
    for x in configs:
        str = str.replace('{{v::' + x + '}}', getConfig(x, ''))
        str = str.replace('{{var::' + x + '}}', getConfig(x, ''))
        str = str.replace('{{vars::' + x + '}}', getConfig(x, ''))
        str = str.replace('{{c::' + x + '}}', getConfig(x, ''))
        str = str.replace('{{config::' + x + '}}', getConfig(x, ''))
        str = str.replace('{{configs::' + x + '}}', getConfig(x, ''))
    return str