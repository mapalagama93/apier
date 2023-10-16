from request_executer import RequestExecuter
import os
import args
import yaml
from termcolor import cprint
from vars import vars
import script_evaluator
import assigner


class Runner:

    def run(self):
        files = self.getFiles()
        if len(files) == 0:
            cprint('No action provided. eg: apier -e=dev action1 action2', 'white', 'on_yellow', attrs=['bold'])
        for x in files:
            cprint('   START ACTION [' + x['name'] + ']   ', 'black', 'on_yellow', attrs=['bold'])


            template = self.getFileContent(x['file'])
            if('preAction' in template):
                context = EvalContext()
                context.this = template
                self.executeSection(template['preAction'], context)
            
            template = self.getFileContent(x['file'])
            executer = RequestExecuter(template)
            if args.is_curl:
                executer.print_curl()
            else:
                executer.execute()
                if not executer.response['success']:
                    code = executer.response['status'] if 'status' in executer.response else 'UNKNOWN STATUS CODE'
                    cprint('Unexpected response code ' + str(code),'red')
                    exit()
                    
                if 'assign' in template:
                    assigner.assign_vars(template['assign'], executer.response)

                if('postAction' in template):
                    context = EvalContext()
                    context.this = template
                    context.response = executer.response
                    self.executeSection(template['postAction'], context)
            
            cprint('   END ACTION [' + x['name']+']   ', 'black', 'on_yellow', attrs=['bold'])
            print('\n')
        
    
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
        data = self.readFile(fpath)
        fileContent = yaml.safe_load(vars.replace_vars(data))
        if 'request' in fileContent and 'bodyContentFile' in fileContent['request']:
            p = os.path.abspath(fileContent['request']['bodyContentFile'])
            if os.path.exists(p):
                bodyContent = self.readFile(p)
                fileContent['request']['body'] = vars.replace_vars(bodyContent)
        return fileContent
    
    def readFile(self, fpath):
        return open(fpath, 'r').read()
    
    def executeSection(self, section, context):
        if 'script' in section:
            script_evaluator.eval(section['script'], context)


class EvalContext:
    pass