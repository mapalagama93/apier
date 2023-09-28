
import initializer
initializer.check_if_init()

import vars
vars.load()
from runner import Runner
run = Runner()
run.run()


