# PyRest

## Description

PyRest is a framework for building simple RESTful web applications with Python.

## Features

1. Super simple setup
2. Class and methods annotations for routing resources
3. Dynamic routing with strict typing
4. Modularization and extensibility (you can extend base class entities and 
add all desired functionality without affecting the work of any other module)
5. Error handling (e.g. schema double registration or invalid schema
parameters)

## QuickStart

1. Import the components you want to use 
2. Create a resource controller class and decorate it with `@RouteController`, 
so that it's recognized by the framework
3. Decorate methods you want to use as request handlers with 
a standard HTTP method name (e.g. `@GET` or `@POST`). Include 
resource schema into the method decorator. A handler **must** accept a request
as the first outer argument or an exception will be raised.  
3. Import and instantiate `PyRest` class, set the 
 app's config parameters and run it to build routing structures and start the server.

```python
from pyrest.app import PyRest
from pyrest.decorators import RouteController, GET
from pyrest.http import HttpRequest, HttpResponse
from pyrest.parser.tree_parser import TreeRouteParser


@RouteController
class UsersController:

    @GET('/users')
    def get_users_list(self, request: HttpRequest) -> HttpResponse:
        print('path: ' + request.path)
        print('users')


    @GET('/users/{id:int}')
    def get_user(self, request: HttpRequest, user_id: int) -> HttpResponse:
        print('path: ' + request.path)
        print('requested user with id ' + str(user_id))



app = PyRest(RouteParserClass=TreeRouteParser)
app.run()

``` 

Now an HTTP server is set up and running, so you can receive 
`GET` requests on all registered schemas!

## Documentation


### Schema

Schema is the main object you'll want to operate, since it defines 
the capabilities of your application. A *route schema* is a string
describing the path to a resource. PyRest supports two kinds of schemas
at the moment: 
- static schemas
- dynamic schemas

**Static schema**

For the handler to be invoked, static schema must be matched by the request URL exactly as written 
in the declaration. 

**Example:**
```python

@RouteController
class MessagesController:

    @GET('/messages/welcome_messages/rules')
    def get_welcome_message_rules(self, request):
        # return rules information

```
For the handler to be invoked, request URL must be the following: 
`/messages/welcome_messages/rules`


**Dynamic schema**

In contrast, dynamic schema is parametrized and can also have strict type    
**Example:**

```python

@RouteController
class UsersController:

    @GET('/users/{id:word}/friends')
    def get_user_friends(self, request, id: str):
        print('I am to list user< ' + str(id) + '> friends!')

```
For the handler to be invoked, any URL with the correct `id`
part can be requested (e.g. `/users/ab_12/friends`)

If parameter is registered with a certain type, PyRest
 will try to match incoming URL string against it and convert to 
 the corresponding python type. 
 
 If a parameter type is mismatched for a correct schema or no schema is registered for the request URL, 
 PyRest will send back 404 response.
   

#### Parameter Types:

1. `int` - same as matching against `\d+` regex, cast to python `int` type
2. `word` - same as matching against `\w+` regex, cast to python `str` type
3. `alpha` - same as matching against `[a-zA-Z]+` regex, cast to python `str` type
4. `any` - same as matching against `.+` regex, cast to python `str` type

If the type isn't specified, `any` is used automatically.

All parameters **must** be written in the following format: `{<name>[:<type>]}`

> *You can extend typing by writing your own RouteParser and adding support for custom route schemas*

### Route Parser

This entity is used to make a URL match your declared schema and call the appropriate handler.

Predefined parsers:
- DefaultRouteParser - makes plain hash mapping `Map: schema -> handler`. Doesn't support 
any cool features like dynamic routing. (located at `pyrest.parsers.default_parser`)
- TreeRouteParser - supports all listed features (located at `pyrest.parsers.tree_parser`)

## Advanced 

If you want to add your own functionality or just curious, how this all works, read on!
### Route Parser

Route Parser is the brain of the whole thing. At construction time, it accepts
a `dict` of the following structure: `route_parser_class -> route_parameters`, where
*route_parameters* is an object, having `http_method`, `class_handler_name`, and 
`schema` attributes. All this information is used to build up a structure that would be
able to resolve routes to resource handlers. 

To make it all work, you extend `AbstractRouteParser`
and implement required methods. After that, pass your superb parser class to `PyRest` 
constructor as follows:
```python
app = PyRest(RouteParserClass=MySuperbParserClass)
``` 
That's all!

### Router 

Router is the entity you're unlikely to run into, but should be aware of. 
Router registers all routes and classes before the app is initialized.
When a new HTTP request is coming, it delegates route resolution and handler invocation to
the route parser. That is why extending PyRest is so simple!