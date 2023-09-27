
# Apier

Elegant API invoker


## Generate
`apier -i -e=dev,uat`
-e parameter specify env files needs to be generated. This command will generate required files and folders in current working directory.


## Common Scripts
Add `scripts_dir`  property to   `config.properties` file to specify common script folder. Apier will load these scripts as modules. 

## Run
`apier -e=dev,dev2 sample1yaml sample2.yaml`
-e command specify env files to be loaded. 