from termcolor import cprint
from pathlib import Path
import args

__sample_request = """name: Sample request
preAction: # this sections is to perform actions before the request.
    # this is inline python script.
    # you can create variables here
    # get('key') can use to get values from vars and configs
    # set('key', 'value') can use to set values to vars
    # importing custom modules from script folder also supported
    # all modules from script folder will be added to path.
    # eg : import function
    # will import function.py from script_dir that defined in config/config.properties 
    # context variable can use to access current file's values. 
    # eg : context.this['name'] will return this file's name 'Sample request'
  script: |
    import vars
    # following line will set values to vars:
    set('customHeader', 'Sample header value')
    set('userId', '2')
request:
  url: "https://en57ezcqeka6h.x.pipedream.net/user/:userId" # to use pathParams in the url use :key
  method: get # support values, get | post | put | delete
  pathParams:
    userId: "{{userId}}" # to use vars and configs as values use {{var_name}}
  queryParams:
    sampleQueryParamKey: "This is query param value"
  basicAuth:  # This add Authorization header for basic auth
    username: sampleUsername
    password: samplePassword
  headers:
    customHeader: "{{customHeader}}"
  requestType: json # default value is json. available values: form | text | json
  responseType: json # default value is json. available values:  text | json
  body: 
  # for request type form body content should be a key value object.
  # key1 : value1
  # key2 : value2
  # for request type json body content can be json string or yaml object
  # for request type string body should be a string
        |
    {
      "key1" : "value1",
      "key2" : "value2"
    }
assign: # assign can use to extract and store values to vars
  body: # body will search values for given jsonPath and store in vars to given key
    userEmail: "$.data.email"
    userFirstName: "$.data.first_name"
  headers: # headers use store response header values in vars
    poweredBy: "X-Powered-By"

postAction: # post action use to perform action after the request. 
  # this is same as preAction script
  # here context will have access to this file as well as response object
  # context.response['headers'] will return response headers
  # context.response['data'] will return response data
  # context.response['json'] will set to True is the response body is a json object
  # context.response['status'] will response status code
  sctips: |
    print('this is post action. response status is', context.response['status'])
"""
class Initializer:

    __files = ['/configs/config.properties', '/configs/vars.properties', '/scripts/functions.py', '/sample.yaml']
    __dirs = ['/configs', '/scripts']
    __file_content = {
            '/sample.yaml' : globals()['__sample_request'],
            '/scripts/functions.py' : "import vars",
            '/configs/config.properties' : "scripts_dir=scripts"
    }

    def init(self):
        self.__files = self.__files + ['/configs/' + x + '.properties' for x in args.env]
        self.create_dirs()
        self.create_files()
        self.write_to_files()

    def create_dirs(self):
        for d in self.__dirs:
            dpath = args.root + d;
            Path(dpath).mkdir(exist_ok=True)
            cprint('create folder ' + dpath, 'green')

    def create_files(self):
        for f in self.__files:
            fpath = args.root + f
            Path(fpath).touch(exist_ok=True)
            cprint('create file ' + fpath, 'green')

    def write_to_files(self):
        for f, content in self.__file_content.items():
            with open(args.root + f, '+a') as file :
                file.write(content)

initializer = Initializer()