from visual_component_plugin import VisualComponentPlugin

sage.misc.latex.latex.add_to_mathjax_avoid_list([r"\multicolumn",r"\verb","None"])

class ListViewPlugin(VisualComponentPlugin):
    def predicate(self, obj):
        return isinstance(obj, (list, tuple))

    template_name = "list_of_linked_objects_template"

    def data(self, obj):
        return obj
ListViewPlugin()

class SageObjectLatexViewPlugin(VisualComponentPlugin):
    def predicate(self, obj):
        return True

    template_name = "sage_object_latex_view_template"

    def data(self, obj):
        s = latex(obj)
        # This logic is about limitations of mathjax; should this it in the template?
        if any(forbidden in s for forbidden in sage.misc.latex.latex.mathjax_avoid_list()
            return None
        return s
SageObjectLatexViewPlugin()

class SageObjectReprViewPlugin(VisualComponentPlugin):
    def predicate(self, obj):
        return True

    template_name = "repr_view_template"

    def data(self, obj):
        repr(obj)
SageObjectReprViewPlugin()

class ElementViewPlugin(VisualComponentPlugin):
    def predicate(self, obj):
        return isinstance(obj, Element)

    template_name = "element_view_template"

    def data(self, obj):
        return obj.parent()

def view_element(self, command):
    return view_sage_object(self, command) + "<br>An element of "+view_sage_object_with_link(self.parent(),command+".parent()")



class CategoryListOfConstructionViewPlugin(...)

    template_name = "list_of_linked_objects"

class CategoryListOfAxiomsViewPlugin(...)

    template_name = "list_of_linked_objects"




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
