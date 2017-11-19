import json


class HttpRequest:

    class RequestMethod:
        post = 'POST'
        get = 'GET'
        update = 'UPDATE'
        delete = 'DELETE'

    methods = RequestMethod()

    def __init__(self, url: str, method: str):
        self.path = None
        self.parameters = None
        self.method = method

        self.parse_url(url)

    def parse_url(self, url: str):
        self.path = url


class HttpResponse:

    def __init__(self, code: int = 200, message: str = 'OK'):
        self.__code = code
        self.__message = message
        self.__headers = dict()
        self.__body = ''

    def add_header(self, header_name: str, header_value: str):
        self.__headers[header_name] = header_value

        return self

    def get_headers(self) -> dict:
        return self.__headers

    def set_body(self, body: str):
        self.__body = body

    def get_body(self) -> bytes:
        return bytes(self.__body, 'utf-8')

    def get_code(self) -> int:
        return self.__code

    def get_message(self):
        return self.__message


class HttpJsonResponse(HttpResponse):

    def __init__(self, json_obj: dict, code: int = 200, message: str = 'OK'):
        super(HttpJsonResponse, self).__init__(code, message)
        self.__json_obj = json_obj
        self.__json_str = json.dumps(json_obj)
        self.add_header('Content-Type', 'application/json')
        self.add_header('Content-Type', 'application/json')
        self.add_header('Content-Length', str(len(self.__json_str)))

        self.set_body(self.__json_str)
