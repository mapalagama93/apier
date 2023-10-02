import args

if args.is_init:
    from initializer import initializer
    initializer.init()
    exit()

import vars

vars.load()
from runner import Runner
run = Runner()
run.run()


