from sage.misc.abstract_method import abstract_method
import sage.misc.latex
from sage.misc.latex import latex
from sage.categories.category import Category
from sage.structure.parent import Parent
from sage.structure.element import Element
from reproducible_object import ReproducibleObject
# Duplicated from sage-explorer

sage.misc.latex.latex.add_to_mathjax_avoid_list(r"\cline")
sage.misc.latex.latex.add_to_mathjax_avoid_list(r"\verb")
sage.misc.latex.latex.add_to_mathjax_avoid_list(r"\multicolumn")
sage.misc.latex.latex.add_to_mathjax_avoid_list("None")

def display_object(sage_object, link=True):
    """
    EXAMPLES::

        sage: from plugins import ReproducibleObject
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
            "data" : [display_object(sage_object[i], link = link) for i in range(len(sage_object.value))]
            }
    s = str(latex(sage_object.value))
    # This logic is about limitations of mathjax; should this it in the template?
    if any(forbidden in s for forbidden in sage.misc.latex.latex.mathjax_avoid_list()):
        result = {
            "style": "text",
            "data" : repr(sage_object.value),
            }
    else:
        result = {
            "style": "latex",
            "data" : s,
            }
    if link:
        result["url"] = sage_object.url()
    return result

active_plugins = []

class VisualComponentPlugin:
    def __init__(self):
        active_plugins.append(self)

    @abstract_method
    def predicate(self, obj):
        """
        Returns whether this plugin applies for the given object obj

        EXAMPLES::

            sage: TODO # todo: not implemented
        """

    @abstract_method
    def render(self, obj):
        """
        Render the plugin for the given object obj

        EXAMPLES::

            sage: TODO # todo: not implemented
        """

def invariants(obj):
    """
    EXAMPLES::

        sage: invariants(ReproducibleObject('1'))
        [{'style': 'invariant_parent',
          'data': {'style': 'latex', 'data': '\\Bold{Z}'}}]
        sage: invariants(ReproducibleObject('DihedralGroup(2)')
        [{'style': 'invariant_category',
          'data': {'style': 'latex', 'data': '\\mathbf{FinitePermutationGroups}'}},
         {'style': 'invariant',
          'data': {'style': 'latex',
                   'data': '{\\setlength{\\arraycolsep}{2\\ex}\n\\begin{array}{r|*{4}{r}}\n\\multicolumn{1}{c|}{\\ast}&a&b&c&d\\\\\\hline\n{}a&a&b&c&d\\\\\n{}b&b&a&d&c\\\\\n{}c&c&d&a&b\\\\\n{}d&d&c&b&a\\\\\n\\end{array}}'},
                   'name': 'multiplication_table'}
        ]
    """
    return [plugin.render(obj)
            for plugin in active_plugins if plugin.predicate(obj)]

class ParentPlugin(VisualComponentPlugin):
    def predicate(self, obj):
        return isinstance(obj.value, Element)

    def render(self, obj):
        return {
            "style": "invariant_parent",
            "data" : display_object(obj.parent()),
            }
ParentPlugin()

class CategoryPlugin(VisualComponentPlugin):
    def predicate(self, obj):
        return isinstance(obj.value, Parent)

    def render(self, obj):
        return {
            "style": "invariant_category",
            "data" : display_object(obj.category()),
            }
CategoryPlugin()

class Invariant(VisualComponentPlugin):
    def __init__(self, invariant, predicate):
        VisualComponentPlugin.__init__(self)
        self._invariant = invariant
        if isinstance(predicate, Category):
            predicate = predicate.__contains__
        self._predicate = predicate

    def predicate(self, obj):
        return self._predicate(obj.value)

    def render(self, obj):
        return {
            "style": "invariant",
            "name" : self._invariant,
            "data" : display_object(obj.multiplication_table()),
            }

from sage.categories.finite_enumerated_sets import FiniteEnumeratedSets
from sage.categories.finite_semigroups import FiniteSemigroups

Invariant("multiplication_table", lambda x: x in FiniteSemigroups() and x.cardinality() < 10);
Invariant("cardinality", FiniteEnumeratedSets());
