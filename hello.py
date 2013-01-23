from flask import Flask
from sage.all import *

app = Flask(__name__)

@app.route("/<command>")
def header():
  return """
  <head>
  <script type="text/x-mathjax-config">
    MathJax.Hub.Config({tex2jax: {inlineMath: [['$','$'], ['\\(','\\)']]}});
  </script>
  <script type="text/javascript"
    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
  </script>
  </head>
  """

def hello(command):
  return "<body>" + str(eval(command)) + "</body>"

if __name__ == "__main__":
  app.run()
