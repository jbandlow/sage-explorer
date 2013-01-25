import inspect
from flask import Flask
from flask import Markup
from flask import render_template
import sagenb.misc.support
import sage.misc.sageinspect
from plugins import display_object
import plugins
from reproducible_object import ReproducibleObject

app = Flask(__name__)

EXAMPLES = [
    "Partition([3,3,2,1])",
    "Permutations(5)",
    "DihedralGroup(6)",
    "EllipticCurve('37b2')",
    "Crystals().example()",
    "HopfAlgebrasWithBasis(QQ).example()",
    ]

@app.route("/<sage_command>")
def explore(sage_command):
    """
    TODO
    """
    sage_output = ReproducibleObject(sage_command)
    return render_template(
        'template.html',
        sage_command   = sage_output.command,
        object_data    = display_object(sage_output, link=False),
        object_help    = display_help(sage_output),
        object_methods = display_methods(sage_output),
        invariants     = plugins.invariants(sage_output),
        )

@app.route("/")
def front_page():
    example_data = []
    for command in EXAMPLES:
        data = display_object(ReproducibleObject(command))
        data['command'] = command
        example_data.append(data)
    return render_template('index.html', example_data=example_data)


def display_help(sage_output):
    return sagenb.misc.support.docstring("x", {"x": sage_output.value})


def display_methods(sage_output):
    return {"style": "method_list",
            "data" : [ {"data": method,
                        "url" : sage_output.url()+"."+method+"()"}
                       for method in argument_less_methods_of_object(sage_output.value)]}


def is_argument_less_method(f):
    """
    EXAMPLES::

    sage: is_argument_less_method(1.factor)
    True
    sage: is_argument_less_method(1.is_idempotent)
    True
    """
    try:
        arg_spec = sage.misc.sageinspect.sage_getargspec(f)
    except:
        return False
    l = len(arg_spec.args)
    if arg_spec.defaults is not None:
        l -= len(arg_spec.defaults)
        return l == 1


def argument_less_methods_of_object(x):
    """
    Returns the list of the names of the methods of ``x`` that take no argument, excluding _methods

    EXAMPLES::

    sage: argument_less_methods_of_object(1)
    ['is_idempotent']
    """
    return [ key
             for (key, f) in inspect.getmembers(x, inspect.isroutine)
             if not key[0] == "_" and is_argument_less_method(f) ]


# Stupid test that we are not running within Sage
if not "Permutations" in globals() and __name__ == "__main__":
        app.run(debug=True)
