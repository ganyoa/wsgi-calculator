""" ag cd Desktop/Python_UW/py_230/L04/assignment/wsgi-calculator
For your homework this week, you'll be creating a wsgi application of
your own.

You'll create an online calculator that can perform several operations.

You'll need to support:

  * Addition
  * Subtractions
  * Multiplication
  * Division

Your users should be able to send appropriate requests and get back
proper responses. For example, if I open a browser to your wsgi
application at `http://localhost:8080/multiple/3/5' then the response
body in my browser should be `15`.

Consider the following URL/Response body pairs as tests:

```
  http://localhost:8080/multiply/3/5   => 15
  http://localhost:8080/add/23/42      => 65
  http://localhost:8080/subtract/23/42 => -19
  http://localhost:8080/divide/22/11   => 2
  http://localhost:8080/               => <html>Here's how to use this page...</html>
```

To submit your homework:

  * Fork this repository (Session03).
  * Edit this file to meet the homework requirements.
  * Your script should be runnable using `$ python calculator.py`
  * When the script is running, I should be able to view your
    application in my browser.
  * I should also be able to see a home page (http://localhost:8080/)
    that explains how to perform calculations.
  * Commit and push your changes to your fork.
  * Submit a link to your Session03 fork repository!


"""
import traceback

def add(*args):
    """ Returns a STRING with the sum of the arguments """
    result = int(args[0]) + int(args[1])
    return str(result)


def subtract(*args):
    result = int(args[0]) - int(args[1])
    return str(result)


def multiply(*args):
    result = int(args[0]) * int(args[1])
    return str(result)


def divide(*args):
    result = int(args[0]) / int(args[1])
    return str(result)


def instructions():
  return """
<head>
<title>Instructions</title>
</head>
<body>
<h1><u>Instructions</u></h1>
<p>
You can preform basic addition, subtraction, multiplication, and division by<br>
modifing the end of the URL. Include 'add', 'subtract', 'multiply', or 'divide',<br>
'/', followed by two numbers, also seperated with a forward slash.<br>
See below for examples.<br>
</p>
<p>Examples:</p>
<p>
  http://localhost:8080/multiply/3/5  => 15<br>
  http://localhost:8080/add/23/42  => 65<br>
  http://localhost:8080/subtract/23/42  => -19<br>
  http://localhost:8080/divide/22/11  => 2<br>
  http://localhost:8080/ => instructions page (here)<br>
</p>
</body>
"""

def resolve_path(path):
    """
    Should return two values: a callable and an iterable of arguments.
    """
    funcs = {
        '': instructions,
        'add': add,
        'subtract': subtract,
        'multiply': multiply,
        'divide': divide
    }

    # TODO: Provide correct values for func and args. The
    # examples provide the correct *syntax*, but you should
    # determine the actual values of func and args using the
    # path.
    path = path.strip('/').split('/') # breaks ulr at slashes

    func_name = path[0] #example: book
    args = path[1:] # id1 or id2

    try:
        func = funcs[func_name] # try to fund function inside the above funcs dict
    except KeyError:
        raise NameError

#    try:
#        if func_name == divide:
#            if args[1] == 0:
#                raise ZeroDivisionError
    #func = add
    #args = ['25', '32']

    return func, args


def application(environ, start_response):
    # TODO: Your application code from the book database
    # work here as well! Remember that your application must
    # invoke start_response(status, headers) and also return
    # the body of the response in BYTE encoding.
    #
    # TODO (bonus): Add error handling for a user attempting
    # to divide by zero.
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
    except ZeroDivisionError:
        status = "500 Internal Server Error"
        body = "<h1>Attempt to divide by zero Error</h1>"
    except Exception:
        status = "500 Internal Server Error"
        body = "<h1>Internal Server Error</h1>"
        print(traceback.format_exc())
    finally:
        headers.append(('Content-length', str(len(body))))
        start_response(status, headers)
        return [body.encode('utf8')]

if __name__ == '__main__':
    # TODO: Insert the same boilerplate wsgiref simple
    # server creation that you used in the book database.
    from wsgiref.simple_server import make_server
    srv = make_server('localhost', 8080, application)
    srv.serve_forever()