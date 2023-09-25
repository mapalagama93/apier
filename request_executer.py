from requests import request
from termcolor import cprint, colored
import json

class RequestExecuter:

    requestTemplate = None
    request = None
    response = None

    def __init__(self, requestTemplate):
        self.requestTemplate = requestTemplate
        self.request = requestTemplate['request']
    
    def execute(self):
        self.log_request()
        try:
            data = self.data() if not self.isJsonRequest() else None
            jsonData = json.loads(self.data()) if self.isJsonRequest() and self.data() != None else None
            res = request(self.method(), self.url(), data=data, 
                        json=jsonData, headers=self.headers())
            self.response = {
                'headers' : dict(res.headers),
                'status' : res.status_code
            }

            self.response['json'] = False
            if self.isJsonResponse():
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
        cprint(' REQUEST ', 'white', 'on_blue')
        print(colored(self.method().upper(), 'blue', attrs=['bold']), colored(self.url(), attrs=['bold']))
        print(colored('Request Headers ', 'magenta', attrs=['bold']),  '\n',  json.dumps(self.headers(), indent=2), sep="")
        print(colored('Request Body ', 'magenta', attrs=['bold']), colored('[JSON]' if self.isJsonRequest() else '', 'light_grey', attrs=['bold']), '\n', json.dumps(json.loads(self.data()), indent=2) if self.isJsonRequest() and self.data() != None else self.data(), sep="")
        print('\n')
    
    def log_response(self):
        cprint(' RESPONSE ', 'white', 'on_green')
        print(colored('Status', 'magenta', attrs=['bold']), self.response['status'])
        print(colored('Response Headers ', 'magenta', attrs=['bold']), '\n' , json.dumps(self.response['headers'], indent=2))
        print(colored('Response Body ', 'magenta', attrs=['bold']), '\n', json.dumps(self.response['data'], indent=2) if self.isJsonResponse() and self.response['json'] else self.response['data'], sep="")
        print('\n')

    def url(self):
        return self.request['url']

    def method(self):
        return self.request['method']

    def data(self):
        return self.request['body'] if 'body' in self.request else None

    def isJsonRequest(self):
        if 'requestType' in self.request:
            return self.request['requestType'] == 'json'
        return True

    def isJsonResponse(self):
        if 'responseType' in self.request:
            return self.request['responseType'] == 'json'
        return True
    
    def headers(self):
        return self.request['headers'] if 'headers' in self.request else {}
    
    