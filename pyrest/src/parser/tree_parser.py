import re

from pyrest.http import HttpRequest
from pyrest.src.controller import PyRestRouteController
from pyrest.src.exceptions import *
from pyrest.src.parser.route_parser import AbstractRouteParser
from pyrest.src.route import RouteParameters


class RegexRouteParser(AbstractRouteParser):

    def resolve(self, request: HttpRequest) -> None:
        pass


# /users/{id:int}

# (\w+(-\w)*)|{\w+(:(number|word|string))?}


schema_pattern = r"^(\/\w+(-\w+)*)|(\/{\w+(:(int|word|alpha))?})$"
parameter_pattern = r"^{\w+(:(int|word|alpha))?}$"
resource_name_pattern = r"^(\w+(-\w+)*)$"


class TreeNode:

    def __init__(self, name: str, is_route: bool=False):
        self.is_route = is_route
        self.name = name
        self.children = dict()
        self.parameter_node = None
        self.route_controller = None
        self.schema = ''
        self.handlers = dict()

    def get_children(self) -> dict:
        return self.children

    def add_child(self, child):
        if self.children.get(child.name, None) is None:
            self.children[child.name] = child

    def get_child(self, child_name):
        return self.children.get(child_name, None)

    def add_parameter(self, parameter_node):
        self.parameter_node = parameter_node

    def get_parameter(self):
        return self.parameter_node

    def add_handler(self, http_method: str, handler):
        if self.handlers.get(http_method, None) is None:
            self.handlers[http_method] = handler
        else:
            raise DoubleMethodBindingError('Http method ' + http_method +
                                           ' already defined for schema ' + self.schema)


class ParamTreeNode(TreeNode):

    def __init__(self, name: str, value_type: str, is_route: bool=False):
        super(ParamTreeNode, self).__init__(name, is_route)
        self.value_type = {
            'int': int,
            'alpha': str,
            'word:': str
        }.get(value_type)

        self.value_pattern = {
            'int': r"\d+",
            'alpha': r"[a-zA-Z]+",
            'word': r""
        }.get(value_type)

    def parse(self, param_string: str):
        if re.match(self.value_pattern, param_string):
            return self.value_type(param_string)

        raise InvalidParameterValueError('Error for schema ' + self.schema +
                                         ': invalid parameter value - ' + param_string)


class TreeRouteParser(AbstractRouteParser):

    def __init__(self, class_routes: dict):
        self._routes_tree = None
        self.__build_routes(class_routes)

    def resolve(self, request: HttpRequest) -> None:
        url = str(request.path)

        if url == '/':
            print('root requested')
            return

        param_values = []
        is_param_value_invalid = False
        invalid_param_value_error = None

        url_parts = url.split('/')
        url_parts[0] = '/'
        node = self._routes_tree
        for i in range(1, len(url_parts)):
            child = node.get_child(url_parts[i])
            if child:
                node = child
            else:
                param = node.get_parameter()
                if not param:
                    raise NoRouteFoundError('Page not found: ' + url)
                try:
                    value = param.parse(url_parts[i])
                    param_values.append(value)
                except InvalidParameterValueError as e:
                    print(repr(e))
                    is_param_value_invalid = True
                    invalid_param_value_error = e
                node = param

        if not node.is_route:
            raise NoRouteFoundError('Page not found: ' + url)

        if is_param_value_invalid:
            raise invalid_param_value_error

        handler = node.handlers.get(request.method, None)
        if not handler:
            raise MethodNotDefinedError('Method ' + request.method + ' is not defined')

        getattr(node.route_controller, handler)(request, *param_values)


    def __build_routes(self, class_routes: dict):
        print('\n\nbuilding tree\n\n')
        for controller_class, route_params_list in class_routes.items():
            controller_instance = controller_class()
            for route_params in route_params_list:
                self.__insert_in_tree(controller_instance, route_params)

        self.__print_tree()

    def __insert_in_tree(self, controller_instance: PyRestRouteController, params: RouteParameters):
        print("Inserting schema: " + params.schema)

        schema = params.schema
        if len(schema) == 0:
            raise InvalidSchemaFormatError('Schema length must be greater that zero')

        current_tree_node = self._routes_tree
        schema_part = schema[0]

        if schema_part != '/':
            raise InvalidSchemaFormatError('Route schema must begin with /')

        if current_tree_node is None:
            # if tree route is not initialized, initialize it
            current_tree_node = TreeNode('/')
            self._routes_tree = current_tree_node

        schema_parts = schema.split('/')

        schema_parts_count = len(schema_parts)

        for i in range(1, schema_parts_count):
            schema_part = str(schema_parts[i])
            print(schema_part)
            if len(schema_part) == 0 and schema != '/':
                raise InvalidSchemaFormatError('Repeating slashes are not allowed')

            if re.match(resource_name_pattern, schema_part):
                print('matched resource name')
                tree_node = current_tree_node.get_child(schema_part)
                if not tree_node:
                    tree_node = TreeNode(schema_part)
                current_tree_node.add_child(tree_node)
                current_tree_node = tree_node
            elif re.match(parameter_pattern, schema_part):
                param_node = current_tree_node.get_parameter()
                if not param_node:
                    value_type = self.__get_value_type(schema_part)
                    param_node = ParamTreeNode(schema_part, value_type)
                else:
                    raise RuntimeError('Error for schema ' + schema +
                                       ': any route part can only contain one parametrized child.')
                current_tree_node.add_parameter(param_node)
                current_tree_node = param_node
                print('matched parameter pattern')
            else:
                raise InvalidSchemaFormatError('Schema part didn\'t match any valid patterns: ' + schema_part)

        if current_tree_node.is_route:
            raise SchemaDoubleDefinitionError('Schema ' + schema + ' already registered')

        current_tree_node.is_route = True
        current_tree_node.schema = schema
        current_tree_node.route_controller = controller_instance
        current_tree_node.add_handler(params.http_method, params.handler)

    def __get_value_type(self, schema_part: str):
        value_type_string = schema_part[schema_part.find(':')+1:-1]
        print(value_type_string)
        return value_type_string

    def __print_tree(self):
        print('\n\n**** printing tree ****\n\n')
        nodes_queue = []

        if self._routes_tree is not None:
            nodes_queue.append(self._routes_tree)

        while len(nodes_queue) > 0:
            node = nodes_queue.pop(0)
            print(node.name)
            children = node.get_children()

            if children is None:
                continue

            for schema, child in children.items():
                nodes_queue.append(child)

            parameter = node.get_parameter()
            if parameter:
                nodes_queue.append(parameter)
