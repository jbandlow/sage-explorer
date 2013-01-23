from flask import Flask
from sage.all import *

app = Flask(__name__)

@app.route("/<command>")
def hello(command):
  return """
  <head>
  <script type="text/x-mathjax-config">
    MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
  </script>
  <script type="text/javascript"
    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
  </script>
  </head>
  <body>
  """ + "$$" + str(eval(command)) + "$$" + "</body>"

def argument_less_methods_of_object(x):
  """
  Returns the list of the names of the methods of ``x`` that take no argument, excluding _methods
  """
  [ key for (key, f) in inspect.getmembers(x, inspect.ismethod) if len(inspect.getargspec(f).args)==1 and not key[0] == "_"]


if __name__ == "__main__":
  app.run()
