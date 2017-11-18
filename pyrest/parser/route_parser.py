from pyrest.http import HttpRequest
from pyrest.src.exceptions import DoubleMethodBindingError, MethodNotDefinedError, NoRouteFoundError
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
