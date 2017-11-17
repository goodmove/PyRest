from pyrest.http import HttpRequest
from pyrest.src.route import RouteParameters
from pyrest.src.route_parser import DefaultRouteParser


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
    INITIALIZING=1
    ROUTING=2


@Singleton
class Router:
    """
        Defines basic routing interface
    """
    def __init__(self):
        # route_controller --> (class_method, http_method, resource_path_schema) mapping
        self._class_routes = dict()
        # instance that parses schemas
        self._route_parser = None
        # router state, which changes while application
        # runtime stages change
        self._state = State.GATHERING

        self._registered_schemas = set()

    # make thread-safe?
    def resolve(self, request: HttpRequest) -> None:
        if self._route_parser:
            self._route_parser.resolve(request)
        else:
            raise ReferenceError('RouteParser is not initialized in router')

    # make thread-safe?
    def register_schema(self, route_controller_class, route_parameters: RouteParameters) -> None:
        if self._state is not State.GATHERING:
            raise AssertionError('Registration is not allowed any more: router has registered all routes.')

        if route_parameters.schema in self._registered_schemas:
            raise RuntimeError('Schema ' + str(route_parameters.schema) + ' is already registered')

        print("Registered schema " + str(route_parameters.schema) + " for class " + str(route_controller_class))

        self._registered_schemas.add(route_parameters.schema)
        class_routes = self._class_routes.get(route_controller_class, [])
        class_routes.append(route_parameters)
        self._class_routes[route_controller_class] = class_routes

    def init_routes(self, route_parser_class=DefaultRouteParser) -> None:
        """
        Instantiates route parser, passes all registered schemas
        to it and switches state to ROUTING to indicate that all routes
        have been initialized and can now be resolved

        :param route_parser_class: route parser class to use to resolve all
            routes, coming with http requests

        :return: void
        """

        if self._state is not State.GATHERING:
            raise AssertionError('All registered routes are already initialized')

        self._state = State.INITIALIZING
        print(str(self._class_routes))
        self._route_parser = route_parser_class(self._class_routes)
        self._state = State.ROUTING


