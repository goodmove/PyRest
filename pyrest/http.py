import json
from email.message import Message


class HttpRequest:

    class RequestMethod:
        post = 'POST'
        get = 'GET'
        update = 'UPDATE'
        delete = 'DELETE'

    methods = RequestMethod()

    def __init__(self, url: str, method: str, headers: Message):
        self.path = None
        self.query_params = dict()
        self.method = method
        self.headers = headers

        self.__parse_url(url)

    def __parse_url(self, url: str):
        url_parts = url.split('?')
        self.path = url_parts[0]

        if len(url_parts) == 1:
            return

        for parameter in url_parts[1].split('&'):
            try:
                (key, value) = parameter.split('=')
                self.query_params[key] = value
            except ValueError as err:
                continue


class HttpJsonRequest(HttpRequest):

    def __init__(self, url: str, method: str, headers: Message, json_body: dict):
        super(HttpJsonRequest, self).__init__(url, method, headers)
        self.__json_body = json_body

    def get_json(self):
        return self.__json_body


class HttpResponse:

    DEFAULT_ENCODING = 'UTF-8'

    def __init__(self, code: int = 200, message: str = 'OK'):
        self.__code = code
        self.__message = message
        self.__headers = dict()
        self.__body = ''
        self.__encoding = HttpResponse.DEFAULT_ENCODING

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

    def set_encoding(self, encoding: str ):
        self.__encoding = encoding

        return self


class HttpJsonResponse(HttpResponse):

    def __init__(self, json_obj: dict, code: int = 200, message: str = 'OK'):
        super(HttpJsonResponse, self).__init__(code, message)
        self.__json_obj = json_obj
        self.__json_str = json.dumps(json_obj)
        self.add_header('Content-Type', 'application/json')
        self.add_header('Content-Type', 'application/json')
        self.add_header('Content-Length', str(len(self.__json_str)))

        self.set_body(self.__json_str)


class ContentType:
    json = 'application/json'
    xml = 'application/xml'
    text = 'text/plain'
    css = 'text/css'
    html = 'text/html'


class Headers:
    content_type = 'Content-Type'
    content_length = 'Content-Length'
