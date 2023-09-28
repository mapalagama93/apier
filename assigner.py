import vars
import jsonpath_ng
from termcolor import cprint 

def assign_body(body, response):
    if response['json']:
        json_data = response['data']
        for x in body:
            try:
                p = jsonpath_ng.parse(body[x])
                match = p.find(json_data)
                if len(match) > 0:
                    vars.set(x, str(match[0].value))
            except jsonpath_ng.exceptions.JsonPathParserError:
                cprint('Cannot parse json path ' + body[x], 'red')
            


def assign_headers(headers, response):
    for x in headers:
        if headers[x] in response['headers']:
            vars.set(x, response['headers'][headers[x]])

def assign_vars(assign, response):
    if 'body' in assign:
        assign_body(assign['body'], response)
    if 'headers' in assign:
        assign_headers(assign['headers'], response)
