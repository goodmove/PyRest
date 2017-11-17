from src.controller import PyRestRouteController
from src.http import HttpRequest
from src.route import RouteParameters
from src.router import Router


def decorate_with_route_info(func, schema: str, http_method: str):
    print('http method decorator called')
    func.schema = schema
    func.http_method = http_method

    return func


def GET(schema: str):
    def decorator(func):
        return decorate_with_route_info(func, schema, HttpRequest.RequestMethod.get)

    return decorator

def POST(schema: str):
    def decorator(func):
        return decorate_with_route_info(func, schema, HttpRequest.RequestMethod.post)

    return decorator

def UPDATE(schema: str):
    def decorator(func):
        return decorate_with_route_info(func, schema, HttpRequest.RequestMethod.update)

    return decorator

def DELETE(schema: str):
    def decorator(func):
        return decorate_with_route_info(func, schema, HttpRequest.RequestMethod.delete)

    return decorator


def inherit_route_controller(cls):
    decorated_class = type(cls.__name__, (PyRestRouteController,) + cls.__bases__, dict(cls.__dict__))
    return decorated_class


def RouteController(class_obj):
    print('___start')
    class_obj = class_obj
    print(class_obj)

    for method_name in dir(class_obj):
        if not method_name.startswith('_'):
            attr = getattr(class_obj, method_name)
            print('method name: ' + method_name)
            schema = getattr(attr, 'schema', None)
            http_method = getattr(attr, 'http_method', None)
            if isinstance(schema, str):
                print(schema)
                delattr(attr, 'schema')
            if isinstance(http_method, str):
                print(http_method)
                delattr(attr, 'http_method')

            Router().register_schema(class_obj, RouteParameters(method_name, http_method, schema))

    print('___end')

    return class_obj
