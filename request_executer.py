from requests import request
from termcolor import cprint, colored
import json
from urllib.parse import urlencode
import args
import base64

class RequestExecuter:

    requestTemplate = None
    request = None
    response = None

    def __init__(self, requestTemplate):
        self.requestTemplate = requestTemplate
        self.request = requestTemplate['request']
    
    def execute(self):        
        self.__log_request()
        try:
            data = self.__data() if not self.__is_json_request() else None
            json = self.__json() if self.__is_json_request() else None            
            self.response = self.__send_request(self.__method(), self.__url(), data, json, self.__headers())
            self.__validate_response()
            self.__log_response()
        except:
            cprint(' ERROR WHILE SENDING REQUEST ', 'red')
            print('\n')
    
    def __send_request(self, method, url, data, json, headers):
        res = request(method, url, data=data, json=json, headers=headers)
        response = {
                'headers' : dict(res.headers),
                'status' : res.status_code
            }
        response['json'] = False
        if self.__is_json_response():
            try:
                response['data'] = res.json()
                response['json'] = True
            except:
                response['data'] = res.text
        else:
            response['data'] = res.text
        return response

    def __validate_response(self):
        self.response['success'] = True
        if 'expectedStatus' in self.request:
            self.response['success'] = self.request['expectedStatus'] == self.response['status']
        
    def __log_request(self):
        cprint(' REQUEST ', 'black', 'on_blue')
        data = self.__body_str()
        print(colored(self.__method().upper(), 'blue', attrs=['bold']), colored(self.__url(), attrs=['bold']))
        print(colored('Request Headers ', 'magenta', attrs=['bold']),  '\n',  json.dumps(self.__headers(), indent=2), sep="")
        print(colored('Request Body ', 'magenta', attrs=['bold']), 
              colored('[JSON]' if self.__is_json_request() and self.__data() != None else '', 'light_grey', attrs=['bold']), '\n', 
              data, sep="")
    
    def __log_response(self):
        cprint(' RESPONSE ', 'black', 'on_green')
        print(colored('Status', 'magenta', attrs=['bold']), self.response['status'])
        print(colored('Response Body ', 'magenta', attrs=['bold']), '\n', 
              json.dumps(self.response['data'], indent=2) if self.__is_json_response() and self.response['json'] else self.response['data'], sep="")
        print(colored('Response Headers ', 'magenta', attrs=['bold']), '\n' , json.dumps(self.response['headers'], indent=2))

    def __url(self):
        return self.__add_path_vars(self.request['url']) + self.__get_query_param()

    def __add_path_vars(self, url):
        if 'pathParams' in self.request:
            for x in self.request['pathParams']:
                url = url.replace(':' + x, str(self.request['pathParams'][x]))
        return url
    
    def __get_query_param(self):
        if 'queryParams' in self.request:
            return '?' + urlencode(self.request['queryParams'])
        return ''

    def __method(self):
        return self.request['method']

    def __data(self):
        return self.request['body'] if 'body' in self.request else None
    
    def __json(self):
        if self.__is_json_request() and self.__data() != None:
            if isinstance(self.__data(), str):
                return json.loads(self.__data())
            return json.loads(json.dumps(self.__data()))
        return None 

    def __body_str(self):
        b_json = self.__json()
        if b_json != None:
            return json.dumps(b_json, indent=2)
        b_data = self.__data()
        if b_data == None:
            return None;
        if isinstance(b_data, str):
            return json.dumps(b_data, indent=2)
        return b_data


    def __is_json_request(self):
        return self.__request_type() == 'json'

    def __is_json_response(self):
        if 'responseType' in self.request:
            return self.request['responseType'] == 'json'
        return True
    
    def __headers(self):
        headers = self.request['headers'] if 'headers' in self.request else {}
        headers['Content-Type'] = self.__content_type()
        if('basicAuth' in self.request):
            headers['authorization'] = self.__basic_auth()
        return headers

    def __basic_auth(self):
        if 'username' in self.request['basicAuth'] and 'password' in self.request['basicAuth']:
            userpass = "{0}:{1}".format(self.request['basicAuth']['username'], self.request['basicAuth']['password'])
            return 'Basic ' + base64.b64encode(userpass.encode()).decode()
        return ''

    def __content_type(self):
        type = self.__request_type()
        if type == 'form':
            return 'form-data/multipart'
        elif type == 'urlencoded':
            return 'application/x-www-form-urlencoded'
        elif type == 'text':
            return 'text/plain'
        return 'application/json'
    
    def __request_type(self):
        return self.request['requestType'] if 'requestType' in self.request else 'json';

    def print_curl(self):
        H = '-H ' if self.__headers() != None else ''
        H += '\n-H '.join(["'{0}: {1}' \\".format(x, self.__headers()[x]) for x in self.__headers()])
        data = self.__curl_body()
        D = ("-d '" + data + "'") if data != None else ''
        print('curl -X ', self.__method().upper(), ' ', self.__url(), ' \\\n', H, '\n', D, ' -kv', sep='' )
    
    def __curl_body(self):
        type = self.__request_type()
        if type == 'form':
            return 'CURL FORM DATA NOT SUPPORT YET'
        elif type == 'urlencoded':
            data = self.__data()
            return data if isinstance(data, str) else urlencode(data)
        elif type == 'text':
            data = self.__data()
            return data if isinstance(data, str) else str(data)
        b_json = self.__json()
        if b_json != None:
            return json.dumps(b_json, indent=2)
        return None 