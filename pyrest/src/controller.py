from pyrest.http import HttpRequest


class PyRestRouteController:

    def __init__(self):
        self.__request = None

    def set_request(self, request: HttpRequest):
        self.__request = request

    def get_request(self) -> HttpRequest:
        return self.__request
