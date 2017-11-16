from src.exceptions import MethodNotDefinedError
from src.http import HttpRequest


class RouteController:

    def __init__(self):
        self.request = None

    def post(self):
        self.__raise_method_not_defined()

    def get(self):
        self.__raise_method_not_defined()

    def update(self):
        self.__raise_method_not_defined()

    def delete(self):
        self.__raise_method_not_defined()

    def set_request(self, request: HttpRequest):
        self.request = request

    def __raise_method_not_defined(self):
        method_not_defined_error_msg = 'Method ' + str(self.request.method) + \
                                            ' is not defined for path ' + str(self.request.path)
        raise MethodNotDefinedError(method_not_defined_error_msg)
