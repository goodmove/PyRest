class NoRouteFoundError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)


class MethodNotDefinedError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)