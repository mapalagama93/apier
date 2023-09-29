from requests import request
from termcolor import cprint, colored
import json
from urllib.parse import urlencode
import args

class RequestExecuter:

    requestTemplate = None
    request = None
    response = None

    def __init__(self, requestTemplate):
        self.requestTemplate = requestTemplate
        self.request = requestTemplate['request']
    
    def execute(self):
        if args.is_curl:
            self.print_curl()
            return

        self.log_request()
        try:
            data = self.data() if not self.is_json_request() else None
            jsonData = self.json() if self.is_json_request() else None            
            res = request(self.method(), self.url(), data=data, 
                        json=jsonData, headers=self.headers())
            self.response = {
                'headers' : dict(res.headers),
                'status' : res.status_code
            }

            self.response['json'] = False
            if self.is_json_response():
                try:
                    self.response['data'] = res.json()
                    self.response['json'] = True
                except:
                    self.response['data'] = res.text
            else:
                self.response['data'] = res.text
            self.log_response()
        except:
            cprint(' ERROR WHILE SENDING REQUEST ', 'red', 'on_red')
            print('\n')
        
    def log_request(self):
        cprint(' REQUEST ', 'black', 'on_blue')
        data = json.dumps(self.json(), indent=2) if self.json() != None else None
        data = json.dumps(self.data(), indent=2) if data == None and not isinstance(self.data(), str) else self.data()
        print(colored(self.method().upper(), 'blue', attrs=['bold']), colored(self.url(), attrs=['bold']))
        print(colored('Request Headers ', 'magenta', attrs=['bold']),  '\n',  json.dumps(self.headers(), indent=2), sep="")
        print(colored('Request Body ', 'magenta', attrs=['bold']), 
              colored('[JSON]' if self.is_json_request() and self.data() != None else '', 'light_grey', attrs=['bold']), '\n', 
              data, sep="")
        print('\n')
    
    def log_response(self):
        cprint(' RESPONSE ', 'black', 'on_green')
        print(colored('Status', 'magenta', attrs=['bold']), self.response['status'])
        print(colored('Response Headers ', 'magenta', attrs=['bold']), '\n' , json.dumps(self.response['headers'], indent=2))
        print(colored('Response Body ', 'magenta', attrs=['bold']), '\n', 
              json.dumps(self.response['data'], indent=2) if self.is_json_response() and self.response['json'] else self.response['data'], sep="")
        print('\n')

    def url(self):
        return self.add_path_vars(self.request['url']) + self.get_query_param()

    def add_path_vars(self, url):
        if 'pathParam' in self.request:
            for x in self.request['pathParam']:
                url = url.replace(':' + x, str(self.request['pathParam'][x]))
        return url
    
    def get_query_param(self):
        if 'queryParam' in self.request:
            return '?' + urlencode(self.request['queryParam'])
        return ''


    def method(self):
        return self.request['method']

    def data(self):
        return self.request['body'] if 'body' in self.request else None
    
    def json(self):
        if self.is_json_request() and self.data() != None:
            if isinstance(self.data(), str):
                return json.loads(self.data())
            return self.data()
        return None 
        

    def is_json_request(self):
        if 'requestType' in self.request:
            return self.request['requestType'] == 'json'
        return True

    def is_json_response(self):
        if 'responseType' in self.request:
            return self.request['responseType'] == 'json'
        return True
    
    def headers(self):
        return self.request['headers'] if 'headers' in self.request else {}
    
    def print_curl(self):
        H = '-H ' if self.headers() != None else ''
        H += '\n-H '.join(['"{0}: {1}" \\'.format(x, self.headers()[x]) for x in self.headers()])
        data = json.dumps(self.json(), indent=2) if self.json() != None else None
        data = json.dumps(self.data(), indent=2) if data == None and not isinstance(self.data(), str) else self.data()
        D = ("-d '" + data + "'") if data != None else ''
    
        print('curl -X ', self.method().upper(), ' ', self.url(), ' \\\n', H, '\n', D, ' -kv', sep='' )



    
    