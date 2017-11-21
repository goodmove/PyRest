import json
from http.server import BaseHTTPRequestHandler

import sys

from pyrest.http import HttpRequest, HttpResponse, HttpJsonRequest, ContentType, Headers
from pyrest.src.exceptions import *
from pyrest.src.router import Router

DEFAULT_SERVER_ADDRESS = ('', 8000)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('new GET request')
        self.__handle_request()

    def do_POST(self):
        print('new POST request')
        content_type = self.headers.get(Headers.content_type)
        http_request = None
        if content_type == ContentType.json:
            content_length = int(self.headers.get(Headers.content_length))
            json_bytes = self.rfile.read(content_length)
            json_obj = json.loads(str(json_bytes, 'UTF-8'))
            http_request = HttpJsonRequest(self.path, self.command, self.headers, json_obj)
        self.__handle_request(http_request)

    def do_UPDATE(self):
        print('new UPDATE request')
        self.__handle_request()

    def do_DELETE(self):
        print('new DELETE request')
        self.__handle_request()

    def __handle_request(self, http_request: HttpRequest = None):
        try:
            if http_request is None:
                http_request = HttpRequest(self.path, self.command, self.headers)
            http_response = Router().resolve(http_request)
        except (NoRouteFoundError,
                MethodNotDefinedError,
                InvalidParameterValueError) as error:
            http_response = HttpResponse(404, 'Not Found. ' + repr(error))
        except Exception as error:
            print(repr(error), file=sys.stderr)
            http_response = HttpResponse(500, 'Internal server error: ' + repr(error))
        self.__send_response(http_response)

    def __send_response(self, http_response: HttpResponse):
        self.send_response(http_response.get_code(), http_response.get_message())
        for name, value in http_response.get_headers().items():
            self.send_header(name, value)
        self.end_headers()

        self.wfile.write(http_response.get_body())
