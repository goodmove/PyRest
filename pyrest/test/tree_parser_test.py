import unittest

from pyrest.parser.tree_parser import TreeRouteParser
from pyrest.src.exceptions import InvalidSchemaFormatError
from pyrest.src.route import RouteParameters


class TreeParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = TreeRouteParser()

        self.static_schemas = [
            '/',
            '/root',
            '/root/level1',
            '/root/level1/level2',
            '/root/level1/level2/level3',
            '/root/dashed-level/level'
            '/root/underscored_level/level'
        ]

        self.dynamic_schemas = [
            '/',
            '/root/{id}',
            '/root1/{param1}/{param2}',
            '/root2/{param1}/level/{param2}',
            '/root3/{param1}/level1/level2/{param2}',
        ]

        self.schemas_with_typing = [
            '/',
            '/root/{id:int}',
            '/root1/{param1:alpha}/{param2:int}',
            '/root2/{param1}/level/{param2:word}',
            '/root3/{param1:int}/level1/level2/{param2:int}',
        ]

        self.invalid_schemas = [
          '',  # empty string
          'root',  # no slashes
          '\\root/level1',  # inverse slash
          '/root+.=?|[]',  # prohibited symbols
          '/root/{}',  # empty parameter definition
          '/root/{123}',  # invalid parameter name (cannot consist of digits only)
          '/root/{{param}}',  # invalid parameter definition
          '/root{id}',  # invalid parameter placement
          '/root/{id}/{id}',  # repeated parameter name
          '/root/{asdf.+?|=[]}',  # invalid parameter format
          '/root/{{p}',  # invalid path format
          '/root/{p}}',  # invalid path format
          '/root{}/{p}',  # invalid path format
          '/root}/{p}',  # invalid path format
          '/{ro{ot/{p}',  # invalid path format
          '/root/{p:qwe}',  # invalid parameter type
        ]



    def test_should_parse_valid_static_schemas(self):
        for schema in self.static_schemas:
            self.assertTrue(self.parser.insert_schema(schema), 'Failed on schema ' + schema)

    def test_should_parse_valid_dynamic_schemas(self):
        for schema in self.dynamic_schemas:
            self.assertTrue(self.parser.insert_schema(schema), 'Failed on schema ' + schema)
    #
    def test_should_parse_valid_dynamic_typing_schemas(self):
        for schema in self.schemas_with_typing:
            self.assertTrue(self.parser.insert_schema(schema), 'Failed on schema ' + schema)

    def test_should_fail_on_invalid_statics(self):
        for schema in self.invalid_schemas:
            self.assertRaises(Exception, self.parser.insert_schema, schema)

unittest.main()