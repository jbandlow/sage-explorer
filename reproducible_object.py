from xml.sax.saxutils import quoteattr
from sage.misc.constant_function import ConstantFunction
from sage.all import *

class ReproducibleObject:
    """
    A wrapper around a Sage object that knows how to reconstruct the object
    """

    def __init__(self, command, value = None):
        self.command = command
        if value is None:
            try:
                value = eval(command)
            except NotImplementedError, e:
                value = "This is not implemented: %s" % e
        self.value = value

    def url(self):
        """
        Returns the URL for this object

        EXAMPLES::

            sage: ReproducibleObject("DihedralGroup(4)").url()
            'http:/DihedralGroup(4)'
        """
        return "http:/"+quoteattr(self.command)[1:-1]

    def __repr__(self):
        return "A Reproducible object"

    def __getattr__(self, key):
        """

        EXAMPLES::

            sage: G = ReproducibleObject("DihedralGroup(4)")
            sage: G.category().command
            'DihedralGroup(4).category()'
            sage: G.category().value
            Category of finite permutation groups
        """
        return ConstantFunction(ReproducibleObject("%s.%s()"%(self.command, key), getattr(self.value, key)()))

    def __getitem__(self, key):
        """

        EXAMPLES::

            sage: G = ReproducibleObject("Permutations(3)")
            sage: G[1].command
            'Permutations(3)[1]'
            sage: G[1].value
            [1, 3, 2]
        """
        return ReproducibleObject("%s[%s]"%(self.command, key), self.value[key])
