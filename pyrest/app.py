from http.server import HTTPServer
from socketserver import ThreadingMixIn

from pyrest.parser.default_parser import DefaultRouteParser
from pyrest.src.pyrest import DEFAULT_SERVER_ADDRESS, RequestHandler
from pyrest.src.router import Router


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

        self.router.init_routes(RouteParserClass)

    def run(self, poll_interval: float=0.5):
        if self.state is not PyRest.State.LAUNCHING:
            raise AssertionError('Server is already running')

        print('Starting server...')
        self.server = HTTPServer(self.server_address, RequestHandler)
        print('Listening at ' + str(self.server_address))
        self.server.serve_forever(poll_interval)