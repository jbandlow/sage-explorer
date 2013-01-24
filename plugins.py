from sage.misc.abstract_method import abstract_method
#from sage_explorer import display_object

# Duplicated from sage-explorer
def display_object(sage_object, command):
    s = latex(sage_object)
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

active_plugins = []

class VisualComponentPlugin:
    def __init__(self):
        active_plugins.append(self)

    @abstract_method
    def predicate(self, obj):
        """
        Returns whether this plugin applies for the given object obj

        EXAMPLES::

            sage: TODO
        """

    @abstract_method
    def render(self, obj):
        """
        Render the plugin for the given object obj

        EXAMPLES::

            sage: TODO
        """

def invariants(obj):
    """
    EXAMPLES::

        sage: invariants(1)
    """
    [plugin.render(obj)
     for plugin in active_plugins if plugin.predicate(obj)]

class ElementViewPlugin(VisualComponentPlugin):
    def predicate(self, obj):
        return isinstance(obj, Element)

    def render(self, obj):
        return {
            "template_name": "invariant_element",
            "data" : display_object(obj.parent()),
            }
ElementViewPlugin()

def view_element(self, command):
    return view_sage_object(self, command) + "<br>An element of "+view_sage_object_with_link(self.parent(),command+".parent()")



#class CategoryListOfConstructionViewPlugin(...)

#    template_name = "list_of_linked_objects"

#class CategoryListOfAxiomsViewPlugin(...)

#    template_name = "list_of_linked_objects"




def view_list(self, command):
    """
    TODO

    EXAMPLES::

    sage: l = [1,2,3,4]
    sage: view_list(l, "l")
    "[<a href='/l[0]'>1</a>,<a href='/l[1]'>2</a>,<a href='/l[2]'>3</a>,<a href='/l[3]'>4</a>]"
    """
    return "[" + ','.join(view_sage_object_with_link(self[i], command+"[%s]"%i) for i in range(len(self))) + "]"

def view_sage_object_with_link(self, command):
    return "<a href=%s>%s</a>" % (quoteattr(command), view_sage_object(self, "/"+command))



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
