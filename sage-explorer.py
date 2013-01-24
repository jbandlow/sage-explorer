import inspect
from flask import Flask
from flask import Markup
from flask import render_template
import sagenb.misc.support
import sage.misc.latex
from sage.misc.latex import latex
#from sage.structure.parent import Parent
#from sage.structure.element import Element


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
    sage_output = eval(sage_command)
    #parent = display_parent(sage_output, command)
    #category = display_category(sage_output, command)
    #object_template, object_content = display_object(sage_output, command)
    #methods = display_methods(sage_output, command)
    return render_template(
        'template.html',
        sage_command = sage_command,
        object_data = display_object(sage_output, sage_command),
        object_help = display_help(sage_output),
        )

# @app.route("/DISABLED")
# def front_page():
#     return render_template('index.html',
#         objects_output = Markup(''.join('<tr><td>'+escape(command)+"</td>" +
#           "<td>"+view_sage_object_with_link(eval(command), command)+"</td></tr>" for command in EXAMPLES)))

def display_object(sage_object, command):
    #if isinstance(obj, (list, tuple)):
    #    return {
    #        "style" = "list",
    #        "data" = map(obj,display_object),
    #        }
    s = latex(sage_object)
    # This logic is about limitations of mathjax; should this it in the template?
    if any(forbidden in s for forbidden in sage.misc.latex.latex.mathjax_avoid_list()):
        return {
            "style": "text",
            "data" : repr(sage_object),
            }
    else:
        return {
            "style": "latex",
            "data" : s,
            }


##############################################################################

# def display_parent(sage_object, command):
#     output = {}
#     if isinstance(sage_object, Element):
#         p = self.Parent()
#         output = {'name': latex_if_possible(p),
#             'link': BASE_URL + '/' + command + '.Parent()'}
#     return output

# def display_category(sage_object, command):
#     output = {}
#     if isinstance(sage_object, Parent):
#         c = self.Category()
#         output = {'name': latex_if_possible(c),
#             'link': BASE_URL + '/' + command + '.Category()'}
#     return output

# def display_template(sage_object):
#     if sage_output in FiniteSemigroups():
#         sage_output.template = 'finite_semigroups'
#         sage_output.content = sage_output.caley_graph()
#     elif isinstance(sage_output, Parent):
#         sage_output.template = 'Parent'
#         sage_output.content = sage_output.caley_graph()
#         object_output = view_parent(sage_output, command)
#     elif isinstance(sage_output, Element):
#         object_output = view_element(sage_output, command)
#     elif isinstance(sage_output, (list, tuple)):
#         object_output = view_list(sage_output, command)
#     else:
#         object_output = view_sage_object(sage_output, command)
#         object_output = Markup(object_output)
#         object_methods_output = Markup(view_sage_object_methods(sage_output, sage_command))
#         help_output = get_help(sage_output)

def display_help(sage_output):
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

# def invariants_view(self, command):
#     """
#     EXAMPLES::

#     sage: print invariants_view(Permutation([2,1]), "foo")
#     <ul>
#     <li><a href='/foo.bruhat_greater()'>bruhat_greater</a>
#     <li><a href='/foo.bruhat_inversions()'>bruhat_inversions</a>
#     ...
#     </ul>
#     """
#     invariants = argument_less_methods_of_object(self)
#     return "<ul>" + " ".join("<li>" + url_generator_for_invariant(invariant, command) for invariant in invariants) + "</ul>"

# def url_generator_for_invariant(invariant, command):
#     # if is_combinatorial:
#     #   style = 'style="color: red";'
#     #   value = ": " + str(eval(command + '.invariant()'))  ## Can we act on the object and not re-eval the command?
#     # else:
#     style = ''
#     value = ''
#     print command, quoteattr(command)
#     return "<a href=\"/%s.%s()\" %s>%s</a>%s" % (quoteattr(command)[1:-1], invariant, style, invariant, value)

# Stupid test that we are not running within Sage
if not "Permutations" in globals():
    from sage.all import *
    if __name__ == "__main__":
        app.run(debug=True)
