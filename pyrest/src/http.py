class HttpRequest:

    class RequestMethod:
        post = 'POST'
        get = 'GET'
        update = 'UPDATE'
        delete = 'DELETE'

    methods = RequestMethod()

    def __init__(self, url: str, method: str):
        self.path = None
        self.parameters = None
        self.method = method

        self.parse_url(url)

    def parse_url(self, url: str):
        self.path = url
