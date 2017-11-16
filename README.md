# PyRest

## Description

PyRest is a framework for bulding simple REST web applications with Python.

## Features

1. Super simple setup
2. Elegant routing for any resources


## QuickStart

1. Import `route` decorator into your project 
2. Define a resource controller class with http methods 
you want ot support
3. import and instantiate `PyRest` class and run the app

```python
from pyrest.app import route
from pyrest.app import PyRest


@route('/articles')
class ArticlesController:
    def get(self):
        print('Articles GET request is received')


app = PyRest()
app.run()

``` 

Now an HTTP server is set up and running, so you can receive 
`GET` requests on `/article` address!