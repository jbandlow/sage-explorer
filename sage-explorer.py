import inspect
from flask import Flask
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
    #parent = display_parent(sage_output, command)
    #category = display_category(sage_output, command)
    #object_template, object_content = display_object(sage_output, command)
    #methods = display_methods(sage_output, command)
    #object_methods = display_methods(sage_output)
    #raise Exception
    return render_template(
        'template.html',
        sage_command   = sage_output.command,
        object_data    = display_object(sage_output, link=False),
        object_help    = display_help(sage_output),
        object_methods = display_methods(sage_output),
        invariants     = plugins.invariants(sage_output),
        )

# @app.route("/DISABLED")
# def front_page():
#     return render_template('index.html',
#         objects_output = Markup(''.join('<tr><td>'+escape(command)+"</td>" +
#           "<td>"+view_sage_object_with_link(eval(command), command)+"</td></tr>" for command in EXAMPLES)))


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
