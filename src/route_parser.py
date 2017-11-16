from src.controller import RouteController
from src.exceptions import MethodNotDefinedError, NoRouteFoundError
from src.network import Request


class AbstractRouteParser:
    """
        Defines interface for all RouteParser implementations.
    """

    def __init__(self, route_mapping):
        self.route_mapping = route_mapping

    def resolve(self, request: Request) -> None:
        """
            Maps request to one of registered RouteController instances

            :param request - HTTP request that was accepted
                by server and passed over to the router
        """
        raise NotImplementedError('Method not implemented in abstract class')


class DefaultRouteParser(AbstractRouteParser):
    """
        Default route parser implementation. Makes trivial
        (route string -> controller) mapping. All routes have been previously
        register by Router instance, which creates instance of this class.
        Doesn't support dynamic routing.
    """

    def __init__(self, route_mapping: dict):
        super(DefaultRouteParser, self).__init__(route_mapping)

    def resolve(self, request: Request):
        route_controller = self.route_mapping.get(request.path, None)

        if route_controller:
            self.__resolve_method(request, route_controller)
        else:
            raise NoRouteFoundError('Route ' + str(request.path) + ' is not registered')

    def __resolve_method(self, request: Request, controller: RouteController):
        requests_map = {
            Request.methods.post: controller.post,
            Request.methods.get: controller.get,
            Request.methods.update: controller.update,
            Request.methods.delete: controller.delete
        }

        handler = requests_map.get(request.method, None)

        controller.set_request(request)

        if handler:
            handler()
        else:
            raise MethodNotDefinedError('Unknown HTTP method: ' + str(request.method))