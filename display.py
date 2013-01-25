import inspect
import sagenb.misc.support
import sage.misc.latex
from sage.misc.latex import latex
from sage.misc.misc import attrcall
from sage.categories.category import Category

sage.misc.latex.latex.add_to_mathjax_avoid_list(r"\cline")
sage.misc.latex.latex.add_to_mathjax_avoid_list(r"\verb")
sage.misc.latex.latex.add_to_mathjax_avoid_list(r"\multicolumn")
sage.misc.latex.latex.add_to_mathjax_avoid_list("None")

def display_object(sage_object, link=True):
    """
    EXAMPLES::

        sage: from reproducible_object import ReproducibleObject
        sage: display_object(ReproducibleObject("1"), link=True)
        {'url': 'http:/1', 'style': 'latex', 'data': '1'}
        sage: display_object(ReproducibleObject("1"), link=False)
        {'style': 'latex', 'data': '1'}
        sage: display_object(ReproducibleObject("Partition([1])"))
        {'url': 'http:/Partition([1])', 'style': 'text', 'data': '[1]'}
        sage: display_object(ReproducibleObject("[1,2,3]"))
        {'style': 'list', 'data': [{'url': 'http:/[1,2,3][0]', 'style': 'latex', 'data': '1'},
                                   {'url': 'http:/[1,2,3][1]', 'style': 'latex', 'data': '2'},
                                   {'url': 'http:/[1,2,3][2]', 'style': 'latex', 'data': '3'}]}
    """
    if isinstance(sage_object.value, (list, tuple)):
        return {
            "style": "list",
            "data" : [display_object(sage_object[i], link = True) for i in range(len(sage_object.value))]
            }
    s = str(latex(sage_object.value))
    # This logic is about limitations of mathjax; should this it in the template?
    if any(forbidden in s for forbidden in sage.misc.latex.latex.mathjax_avoid_list()):
        s = repr(sage_object.value)
        result = {
            "style": "2Dtext" if "\n" in s else "text",
            "data" : s,
            }
    else:
        result = {
            "style": "latex",
            "data" : s,
            }
    if link:
        result["url"] = sage_object.url()
    return result


##############################################################################
# Utility functions

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
    ['N', ..., 'version']
    sage: argument_less_methods_of_object(Partition([2,1]))
    ['N', 'arm_lengths', ..., 'young_subgroup_generators']

    """
    return [ key
             for (key, f) in inspect.getmembers(x, inspect.isroutine)
             if not key[0] == "_" and is_argument_less_method(f) ]

##############################################################################
# Plugin mechanism for the list of properties that are displayed

active_property_displayers = []

class PropertyDisplayer:

    def __init__(self, predicate, invariant, code=None, section=None):
        """

        EXAMPLES::

        """
        active_property_displayers.append(self)
        self._invariant = invariant
        if isinstance(predicate, Category):
            predicate = predicate.__contains__
        elif isinstance(predicate, type):
            predicate = predicate.__instancecheck__
        self._predicate = predicate
        if code is not None:
            if isinstance(code, str):
                self.result = attrcall(code)
            else:
                self.result=code
        else:
            self._method = invariant.lower().replace(" ", "_")

    def predicate(self, obj):
        """
        Returns whether this plugin applies for the given object obj

        EXAMPLES::

            sage: TODO # todo: not implemented
        """
        return self._predicate(obj.value)

    def result(self, obj):
        return getattr(obj, self._method)()

    def display(self, obj):
        """
        Display the property for the given object obj

        EXAMPLES::

            sage: TODO # todo: not implemented
        """
        return {
            "style": "invariant",
            "name" : self._invariant,
            "data" : display_object(self.result(obj)),
            }

def display_properties(obj):
    """
    EXAMPLES::

        sage: property_displayers(ReproducibleObject('1'))
        [{'style': 'invariant_parent',
          'data': {'style': 'latex', 'data': '\\Bold{Z}'}}]
        sage: property_displayers(ReproducibleObject('DihedralGroup(2)')
        [{'style': 'invariant_category',
          'data': {'style': 'latex', 'data': '\\mathbf{FinitePermutationGroups}'}},
         {'style': 'invariant',
          'data': {'style': 'latex',
                   'data': '{\\setlength{\\arraycolsep}{2\\ex}\n\\begin{array}{r|*{4}{r}}\n\\multicolumn{1}{c|}{\\ast}&a&b&c&d\\\\\\hline\n{}a&a&b&c&d\\\\\n{}b&b&a&d&c\\\\\n{}c&c&d&a&b\\\\\n{}d&d&c&b&a\\\\\n\\end{array}}'},
                   'name': 'multiplication_table'}
        ]
    """
    return [plugin.display(obj)
            for plugin in active_property_displayers if plugin.predicate(obj)]


