import inspect
from flask import Flask
import sage.all

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
  """ + "$$" + latex(eval(command)) + "$$" + "</body>"

def argument_less_methods_of_object(x):
  """
  Returns the list of the names of the methods of ``x`` that take no argument, excluding _methods

  EXAMPLES::

      sage: argument_less_methods_of_object(1)
      ['is_idempotent']
  """
  return [ key for (key, f) in inspect.getmembers(x, inspect.ismethod) if len(inspect.getargspec(f).args)==1 and not key[0] == "_"]

def invariants_view(self, command):
    """
    EXAMPLES::

        sage: print invariants_view(Permutation([2,1]), "foo")
        <ul>
        <a href='/foo.bruhat_greater()'>bruhat_greater</a>
        <a href='/foo.bruhat_inversions()'>bruhat_inversions</a>
        ...
        </ul>
    """
    invariants = argument_less_methods_of_object(self)
    return "<ul>\n"+"\n".join("<a href='/%s.%s()'>%s</a>"%(command, invariant, invariant) for invariant in invariants)+"\n</ul>\n"

# Stupid test that we are not running within Sage
if __name__ == "__main__" and not "Permutations" in globals():
  app.run()
