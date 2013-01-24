from sage.misc.abstract_method import abstract_method
import sage.misc.latex
from sage.misc.latex import latex
from sage.categories.semigroups import Semigroups
from sage.structure.parent import Parent
from sage.structure.element import Element
from reproducible_object import ReproducibleObject

# Duplicated from sage-explorer

sage.misc.latex.latex.add_to_mathjax_avoid_list(r"\cline")
sage.misc.latex.latex.add_to_mathjax_avoid_list(r"\verb")
sage.misc.latex.latex.add_to_mathjax_avoid_list(r"\multicolumn")
sage.misc.latex.latex.add_to_mathjax_avoid_list("None")

def display_object(sage_object, link=True):
    #if isinstance(obj, (list, tuple)):
    #    return {
    #        "style" = "list",
    #        "data" = map(obj,display_object),
    #        }
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
    def __init__(self, invariant, category):
        VisualComponentPlugin.__init__(self)
        self._invariant = invariant
        self._category = category

    def predicate(self, obj):
        return obj.value in self._category

    def render(self, obj):
        return {
            "style": "invariant",
            "name" : self._invariant,
            "data" : display_object(obj.multiplication_table()),
            }
Invariant("multiplication_table", Semigroups());

def view_element(self, command):
    return view_sage_object(self, command) + "<br>An element of "+view_sage_object_with_link(self.parent(),command+".parent()")



#class CategoryListOfConstructionViewPlugin(...)

#    style = "list_of_linked_objects"

#class CategoryListOfAxiomsViewPlugin(...)

#    style = "list_of_linked_objects"




# def view_list(self, command):
#     """
#     TODO

#     EXAMPLES::

#     sage: l = [1,2,3,4]
#     sage: view_list(l, "l")
#     "[<a href='/l[0]'>1</a>,<a href='/l[1]'>2</a>,<a href='/l[2]'>3</a>,<a href='/l[3]'>4</a>]"
#     """
#     return "[" + ','.join(view_sage_object_with_link(self[i], command+"[%s]"%i) for i in range(len(self))) + "]"

# def view_sage_object_with_link(self, command):
#     return "<a href=%s>%s</a>" % (quoteattr(command), view_sage_object(self, "/"+command))



def view_sage_object_methods(self, command):
    return invariants_view(self, command)

def view_parent(self, command):
    return view_sage_object(self, command) + "<br>A parent in "+view_sage_object_with_link(self.category(),command+".category()")

def view_finite_semigroup(self, command):
    s = view_parent(self, command)
    if self.cardinality() < 30:
        s += "<br>Multiplication table: <pre>%s</pre>"%(self.cayley_table())
        return s

def view_permutation(self):
    pass
