import args
from jproperties import Properties
from pathlib import Path
import os
from termcolor import cprint

class Vars:
    __configs = Properties()
    __vars = Properties()
    __context = Properties()

    __config_file = args.root + '/configs/config.properties'
    __var_file = args.root + '/configs/vars.properties'
    __env_files = []

    def init(self):
        self.__env_files = [args.root + '/configs/' + file + '.properties' for file in args.env]
        self.__load_config()
        self.__load_vars()
        self.__load_envs()

    def __load_config(self):
        with open(self.__config_file, 'rb') as file:
            self.__configs.load(file, 'utf-8')

    def __load_vars(self):
        with open(self.__var_file, 'rb') as file:
            self.__vars.load(file, 'utf-8')

    def __load_envs(self):
        for fpath in self.__env_files:
            if(os.path.exists(fpath) == False):
                cprint(fpath + ' file does not exists.', 'yellow')
            with open(fpath, 'rb') as file:
                self.__configs.load(file, 'utf-8')

    def __sync_vars(self):
        with open(self.__var_file, 'wb') as file:
            self.__vars.store(file, encoding='utf-8')
    
    def get(self, key, default_alue = ''):
        if key in self.__vars:
            return self.__vars[key].data
        
        if key in self.__configs:
            return self.__configs[key].data

        if key in self.__context:
            return self.__context[key].data
        
        return default_alue

    def set(self, key, value):
        self.__vars[key] = value
        self.__sync_vars()
    
    def get_all(self):
        all = Properties()
        all.update(self.__configs)
        all.update(self.__vars)
        all.update(self.__context)
        return all
    
    def replace_vars(self, text):
        print(type(text))
        for x in self.get_all():
            text = text.replace('{{' + x + '}}', self.get(x, ''))
            text = text.replace('{{v::' + x + '}}', self.get(x, ''))
            text = text.replace('{{vars::' + x + '}}', self.get(x, ''))
        return text
    
    def set_context(self, key, value):
        self.__context[key, value]

     

vars = Vars()