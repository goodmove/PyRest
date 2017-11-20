from http.server import BaseHTTPRequestHandler

import sys

from pyrest.http import HttpRequest, HttpResponse
from pyrest.src.exceptions import *
from pyrest.src.router import Router

DEFAULT_SERVER_ADDRESS = ('', 8000)


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('new GET request')
        self.__handle_request()

    def do_POST(self):
        print('new POST request')
        self.__handle_request()

    def do_UPDATE(self):
        print('new UPDATE request')
        self.__handle_request()

    def do_DELETE(self):
        print('new DELETE request')
        self.__handle_request()

    def __handle_request(self):
        try:
            http_response = Router().resolve(HttpRequest(self.path, self.command))
        except  (NoRouteFoundError,
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
