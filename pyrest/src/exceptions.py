class NoRouteFoundError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)


class MethodNotDefinedError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)


class DoubleMethodBindingError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)


class SchemaDoubleDefinitionError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)


class InvalidSchemaFormatError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)


class InvalidParameterValueError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)

class DoubleDeclarationError(Exception):
    def __init__(self, message, *args):
        super().__init__(message, *args)
