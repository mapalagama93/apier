import args

if args.is_init:
    from initializer import initializer
    initializer.init()
    exit()


from vars import vars
vars.init()
from runner import Runner
run = Runner()
run.run()


