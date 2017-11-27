import json
from http.server import BaseHTTPRequestHandler

import sys

import re

from pyrest.http import HttpRequest, HttpResponse, HttpJsonRequest, ContentType, Headers, ResponseMessages
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
        if re.match(ContentType.json, content_type):
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

    def do_OPTIONS(self):
        self.__send_response(HttpResponse())

    def __handle_request(self, http_request: HttpRequest = None):
        try:
            if http_request is None:
                http_request = HttpRequest(self.path, self.command, self.headers)
            http_response = Router().resolve(http_request)
        except (NoRouteFoundError,
                InvalidParameterValueError) as error:
            http_response = HttpResponse(404, ResponseMessages.messages.get(404))
        except MethodNotDefinedError as error:
            http_response = HttpResponse(405, ResponseMessages.messages.get(405))
        except Exception as error:
            print(repr(error), file=sys.stderr)
            http_response = HttpResponse(500, ResponseMessages.messages.get(500))
        self.__send_response(http_response)

    def __send_response(self, http_response: HttpResponse):
        http_response.add_header('Access-Control-Allow-Origin', '*') \
                    .add_header('Access-Control-Allow-Headers', 'Content-Type, Content-Range, Cache-Control, '
                                                                'Authorization, Keep-Alive, User-Agent') \
                    .add_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_response(http_response.get_code(), http_response.get_message())
        for name, value in http_response.get_headers().items():
            self.send_header(name, value)
        self.end_headers()

        self.wfile.write(http_response.get_body())
