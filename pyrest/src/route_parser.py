from pyrest.src.exceptions import DoubleMethodBindingError, MethodNotDefinedError, NoRouteFoundError
from pyrest.src.http import HttpRequest
from pyrest.src.route import Route


class AbstractRouteParser:
    """
        Defines interface for all RouteParser implementations.
    """
    def resolve(self, request: HttpRequest) -> None:
        """
            Maps request to one of registered RouteController instances

            :param request - HTTP request that was accepted
                by server and passed over to the router
        """
        raise NotImplementedError('Method not implemented in abstract class')


class RouteContainer:

    def __init__(self, route: Route):
        self.route = route
        self.handlers = dict()

    def __hash__(self):
        return self.route.__hash__()

    def add_handler(self, handler, http_method):
        if self.handlers.get(http_method):
            raise DoubleMethodBindingError('Http method ' + str(http_method) + ' for schema' +
                               self.route.get_schema() + ' is already registered')

        self.handlers[http_method] = handler

    def get_handler(self, http_method):
        handler = self.handlers.get(http_method, None)

        if handler is None:
            raise MethodNotDefinedError('No handler is defined for pair (' +
                               self.route.get_schema() + ',' +  http_method + ')')

        return self.route.get_controller(), handler


class DefaultRouteParser(AbstractRouteParser):
    """
        Default route parser implementation. Makes trivial
        (route string -> controller) mapping. All routes have been previously
        register by Router instance, which creates instance of this class.
        Doesn't support dynamic routing.
    """

    def __init__(self, class_routes: dict):
        # routes instances which request path will be matched against
        self._routes = dict()
        # parse schemas and turn them into resolvable routes
        self.__build_routes(class_routes)

    def resolve(self, request: HttpRequest):
        route_container = self._routes.get(request.path, None)

        if not route_container:
            # aka 404 error
            raise NoRouteFoundError('Route ' + str(request.path) + ' is not registered')

        # call controller method, which is bound to certain
        # http request method
        getattr(
            route_container.route.get_controller(),
            route_container.handlers.get(request.method)
        )()

    def __build_routes(self, class_routes: dict):
        for controller_class, route_params_list in class_routes.items():
            controller_instance = controller_class()
            for params in route_params_list:
                route_container = self._routes.get(params.schema, None)

                if route_container is None:
                    route = Route(params.schema, [], controller_instance)
                    route_container = RouteContainer(route)
                    self._routes[params.schema] = route_container

                route_container.add_handler(params.handler, params.http_method)
