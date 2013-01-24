from xml.sax.saxutils import escape, quoteattr
from sage.all import *

class ReproducibleObject:
    """
    A wrapper around a Sage object
    """

    def __init__(self, command, value = None):
        self.command = command
        if value is None:
            self.value = eval(command)

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
        """
        return ConstantFunction(ReproducibleObject("%s.%s()"%(self.command, key), getattr(self.value, key)()))
