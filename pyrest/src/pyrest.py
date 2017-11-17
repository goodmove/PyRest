from http.server import BaseHTTPRequestHandler

from pyrest.http import HttpRequest
from pyrest.src.router import Router


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('new request')
        Router().resolve(HttpRequest(self.path, HttpRequest.methods.get))
        self.send_response_only(200, 'OK')


DEFAULT_SERVER_ADDRESS = ('', 8000)
