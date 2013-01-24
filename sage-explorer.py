import inspect
from flask import Flask
from flask import Markup
from flask import render_template
from sage.structure.parent import Parent
from sage.structure.element import Element

app = Flask(__name__)

@app.route("/<command>")
def explore(command):
    """
    This is responsible for defining object_output (HTML representing the object)
    and optionally object_methods_output (HTML representing methods that can be
    applied to the object).
    """
    sage_output = eval(command)
    # Here we would need a cube-style selector mechanism
    # Runtime type checking for now.
    if sage_output in FiniteSemigroups():
        object_output = view_finite_semigroup(sage_output, command)
    elif isinstance(sage_output, Parent):
        object_output = view_parent(sage_output, command)
    elif isinstance(sage_output, Element):
        object_output = view_element(sage_output, command)
    elif isinstance(sage_output, (list, tuple)):
        object_output = view_list(sage_output, command)
    else:
        object_output = view_sage_object(sage_output, command)
        object_output = Markup(object_output)
        object_methods_output = Markup(view_sage_object_methods(sage_output, command))
        help_output = get_help(sage_output)
        return render_template('template.html', sage_command=command,
                               object_output=object_output, object_methods_output=object_methods_output,
                               help_output=help_output)

examples = [
    "Partition([3,3,2,1])",
    "Permutations(5)",
    "DihedralGroup(6)",
    "EllipticCurve('37b2')",
    "Crystals().example()",
    "HopfAlgebrasWithBasis(QQ).example()",
    ]

@app.route("/")
def front_page():
    return render_template('index.html',
                           objects_output = Markup(''.join('<tr><td>'+escape(command)+"</td>"
                                                           +"<td>"+view_sage_object_with_link(eval(command), command)+"</td></tr>"
                                                           for command in examples)))

def get_help(sage_output):
    return Markup(sagenb.misc.support.docstring("x", {"x": sage_output}))


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

def invariants_view(self, command):
    """
    EXAMPLES::

    sage: print invariants_view(Permutation([2,1]), "foo")
    <ul>
    <li><a href='/foo.bruhat_greater()'>bruhat_greater</a>
    <li><a href='/foo.bruhat_inversions()'>bruhat_inversions</a>
    ...
    </ul>
    """
    invariants = argument_less_methods_of_object(self)
    return "<ul>" + " ".join("<li>" + url_generator_for_invariant(invariant, command) for invariant in invariants) + "</ul>"

def url_generator_for_invariant(invariant, command):
    # if is_combinatorial:
    #   style = 'style="color: red";'
    #   value = ": " + str(eval(command + '.invariant()'))  ## Can we act on the object and not re-eval the command?
    # else:
    style = ''
    value = ''
    print command, quoteattr(command)
    return "<a href=\"/%s.%s()\" %s>%s</a>%s" % (quoteattr(command)[1:-1], invariant, style, invariant, value)

# Stupid test that we are not running within Sage
if not "Permutations" in globals():
    from sage.all import *
    if __name__ == "__main__":
        app.run(debug=True)
