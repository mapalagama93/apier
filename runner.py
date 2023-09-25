from request_executer import RequestExecuter
import os
import args
import yaml
from termcolor import cprint
import store

class Runner:

    def run(self):
        files = self.getFiles()
        for x in files:
            cprint('   START ACTION [' + x['name'] + ']   ', 'white', 'on_yellow')
            print('\n')
            executer = RequestExecuter(self.getFileContent(x['file']))
            executer.execute()
            cprint('   END ACTION [' + x['name']+']   ', 'white', 'on_yellow')
            print('\n\n\n')
        
    
    def getFiles(self):
        contents = []
        for x in args.actions :
            p = os.path.abspath(x)
            if not os.path.exists(p):
                cprint('action file not found ' + p, 'red')
                exit()
            contents.append({
                'file' : p,
                'name' : x
            })
        return contents
    
    def getFileContent(self, fpath):
        with open(fpath, 'r') as file:
            return yaml.safe_load(store.populate(file.read()))