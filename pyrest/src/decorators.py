def decorate_with_route_info(func, schema: str, http_method: str):
    # print('http method decorator called')
    func.schema = schema
    func.http_method = http_method

    return func
