from request_executer import RequestExecuter

class Runner:

    def run(self):
        executer = RequestExecuter({
            'name' : 'register',
            'request' : {
                'url' : 'https://4826f5c6-d528-4658-b833-4b3fe77d9ec5.mock.pstmn.io/api/500',
                'method' : 'get',
                'body' : '{"succcess": "no"}'
            }
        })
        executer.execute()