from sage.misc.abstract_method import abstract_method

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
    def html(self, obj):
        """
        Returns the html rendering for the given object obj

        EXAMPLES::

            sage: TODO
        """
