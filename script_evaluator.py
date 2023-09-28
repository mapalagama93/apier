import vars
import sys
import os



def eval(scriptSection, context):
    if vars.get('scripts_dir') != None:
        sys.path.append(os.path.abspath(vars.get('scripts_dir')))
    set = vars.set
    get = vars.get

    if isinstance(scriptSection, str):
        exec(scriptSection)
    
    if 'file' in scriptSection:
        with open(os.path.abspath(scriptSection['file'])) as f:
            exec(f.read())