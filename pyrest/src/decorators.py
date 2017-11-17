from pyrest.src.controller import PyRestRouteController


def decorate_with_route_info(func, schema: str, http_method: str):
    print('http method decorator called')
    func.schema = schema
    func.http_method = http_method

    return func


def inherit_route_controller(cls):
    decorated_class = type(cls.__name__, (PyRestRouteController,) + cls.__bases__, dict(cls.__dict__))
    return decorated_class
