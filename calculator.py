"""
create an online calculator that can perform several operations.

applications will support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```
"""
def index_page():
    body = ['<h1>Here is how to use this page...</h1>', '<ul>']
    body.append('add/3/5 ==> sum of 3+5</ul>')
    body.append('<ul>subtract/10/2 ==> result of 10-2</ul>')
    body.append('<ul>multiply2/10 ==> result of 2x10</ul>')
    body.append('<ul>divide/20/5 ==> result of 20/2</ul>')
    return '\n'.join(body)

def add(*args):
    """ Returns a STRING with the sum of the arguments """

    sum = 0
    for a in args:
      sum += int(a)
    return str(sum)

def subtract(*args):
  diff = int(args[0]) - int(args[1])
  return str(diff)

def multiply(*args):
  result = int(args[0]) * int(args[1])

  return str(result)

def divide(*args):
  try:
    result = int(args[0]) / int(args[1])
    return str(result)
  except ZeroDivisionError:
    return 'Error! Divide by zero'

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of
    arguments.
    """
    funcs = {
        '':  index_page,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }
    #func = add
    #args = ['25', '32']

    path = path.strip('/').split('/')

    func_name = path[0]
    args = path[1:]
    try:
        func = funcs[func_name]
    except KeyError:
        raise NameError

    return func, args

def application(environ, start_response):

    headers = [("Content-type", "text/html")]
    try:
        path = environ.get('PATH_INFO', None)
        if path is None:
            raise NameError
        func, args = resolve_path(path)
        body = func(*args)
        status = "200 OK"
    except NameError:
        status = "404 Not Found"
        body = "<h1>Not Found</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()
