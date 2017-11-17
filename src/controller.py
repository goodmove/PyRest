from src.exceptions import MethodNotDefinedError
from src.http import HttpRequest


class PyRestRouteController:

    def __init__(self):
        self.request = None

    def set_request(self, request: HttpRequest):
        self.request = request
