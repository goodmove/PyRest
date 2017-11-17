from src.controller import PyRestRouteController


class AbstractRoute:

    def get_schema(self) -> str:
        raise NotImplementedError('get_schema method not implemented')

    def get_parameter_names(self):
        raise NotImplementedError('get_parameter_names method not implemented')

    def __hash__(self):
        raise NotImplementedError('__hash__ method not implemented')


class RouteParameters:
    def __init__(self, handler, http_method, resource_path_schema):
        self.handler = handler
        self.http_method = http_method
        self.schema = resource_path_schema


class Route(AbstractRoute):

    def __init__(self,
                 schema: str,
                 parameter_names: list,
                 controller_instance: PyRestRouteController):
        self._schema = schema
        self._parameter_names = parameter_names
        self._controller = controller_instance

    def get_schema(self):
        return self._schema

    def get_parameter_names(self):
        return self._parameter_names

    def get_controller(self):
        return self._controller

    def __hash__(self):
        return self._schema.__hash__()
