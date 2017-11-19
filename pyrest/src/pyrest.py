from http.server import BaseHTTPRequestHandler

from pyrest.http import HttpRequest
from pyrest.src.router import Router


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('new request')

        http_response = Router().resolve(HttpRequest(self.path, HttpRequest.methods.get))
        self.send_response(http_response.get_code(), http_response.get_message())
        for name, value in http_response.get_headers().items():
            self.send_header(name, value)
        self.end_headers()

        self.wfile.write(http_response.get_body())


DEFAULT_SERVER_ADDRESS = ('', 8000)
