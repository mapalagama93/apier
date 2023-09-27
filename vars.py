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

for ev in args.env:
    env_file_path = args.root + '/' + ev + '.properties'
    if(os.path.exists(env_file_path) == False):
        cprint(ev + '.properties file does not exists.', attrs=['reverse'])
    else:
        env_file = open(env_file_path, 'rb')
        configs.load(env_file, 'utf-8')

vars_file_path = args.root + '/vars.properties'
Path(vars_file_path).touch(exist_ok=True)
var_file = open(vars_file_path, 'rb')
vars.load(var_file, 'utf-8')


def get_config(key, val=None):
    try:
        return configs[key].data
    except:
        return val

def get_var(key, val=None):
    try:
        return vars[key].data
    except:
        return val

def set(key, val):
    vars[key] = val
    with open(vars_file_path, 'wb') as f:
        vars.store(f, encoding='utf-8')

def get(key, val=''):
    return get_config(key, get_var(key, ''))

def get_all():
    all = Properties()
    all.update(configs)
    all.update(vars)
    return all


def populate(str):
    for x in get_all():
        str = str.replace('{{v::' + x + '}}', get_config(x, ''))
        str = str.replace('{{var::' + x + '}}', get_config(x, ''))
        str = str.replace('{{vars::' + x + '}}', get_config(x, ''))
    return str