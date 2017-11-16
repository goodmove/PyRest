from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn

from src.http import HttpRequest
from src.route_parser import DefaultRouteParser
from src.router import Router


class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print('new request')
        Router().resolve(HttpRequest(self.path, HttpRequest.methods.get))
        self.send_response_only(200, 'OK')


DEFAULT_SERVER_ADDRESS = ('', 8000)

class PyRest:

    class State:
        RUNNING = 0
        LAUNCHING = 1

    def __init__(self,
                 server_address=DEFAULT_SERVER_ADDRESS,
                 MixInClass=ThreadingMixIn,
                 RouteParserClass=DefaultRouteParser):
        print('Initializing application...')
        self.server_address = server_address
        self.server = None
        self.state = PyRest.State.LAUNCHING

        self.router = Router()
        self.threading_mixin_class = MixInClass

        self.router.start_routing(RouteParserClass)

    def run(self, poll_interval: float=0.5):
        if self.state is not PyRest.State.LAUNCHING:
            raise AssertionError('Server is already running')

        print('Starting server...')
        self.server = HTTPServer(self.server_address, RequestHandler)
        print('Listening at ' + str(self.server_address))
        self.server.serve_forever(poll_interval)
