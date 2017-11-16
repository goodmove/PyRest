from src.controller import RouteController
from src.router import Router


def route(resource_path):
    # print('decorator: registering path: ' + str(resource_path))

    def decorator(cls):
        cls.path = resource_path
        decorated_class = type(cls.__name__, (RouteController,) + cls.__bases__, dict(cls.__dict__))
        Router().register(resource_path, decorated_class)

        return decorated_class

    return decorator