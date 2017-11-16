from src.network import Request
from src.route_parser import DefaultRouteParser


class Singleton:
    def __init__(self, klass):
        self.klass = klass
        self.instance = None

    def __call__(self,*args, **kwds):
        if self.instance is None:
            self.instance = self.klass(*args, **kwds)
        return self.instance


class State:
    GATHERING=0
    ROUTING=1


@Singleton
class Router:
    """
        Defines basic routing interface
    """
    def __init__(self, ):
        self.routes = dict()
        self.route_parser = None
        self.state = State.GATHERING

    # make thread-safe?
    def resolve(self, request: Request) -> None:
        if self.route_parser:
            self.route_parser.resolve(request)
        else:
            raise ReferenceError('RouteParser is not initialized in router')

    # make thread-safe?
    def register(self, route_schema: str, route_controller_class) -> None:
        if self.state is not State.GATHERING:
            raise AssertionError('Registration is not allowed any more: router has registered all routes.')
        # print("Registered route " + str(route_schema) + " for class " + str(route_controller_class))
        # print('router address: ' + str(self))

        controller = self.routes.get(route_schema, None)
        if controller is None:
            self.routes[route_schema] = route_controller_class()
        else:
            message = 'Cannot assign multiple controllers to one route.\nRoute ' + \
                      str(route_schema) + ' is already registered.'
            raise AssertionError(message)

    def start_routing(self, route_parser_class=DefaultRouteParser) -> None:
        self.state = State.ROUTING
        self.route_parser = route_parser_class(self.routes)
