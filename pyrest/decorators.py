from pyrest.http import HttpRequest
from pyrest.src.decorators import decorate_with_route_info, inherit_route_controller
from pyrest.src.route import RouteParameters
from pyrest.src.router import Router


def RouteController(class_obj):
    print('___start')
    class_obj = class_obj
    inherited_class_obj = inherit_route_controller(class_obj)
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

            Router().register_schema(inherited_class_obj, RouteParameters(method_name, http_method, schema))

    print('___end')

    return inherited_class_obj


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