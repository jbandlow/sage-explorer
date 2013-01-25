from display import PropertyDisplayer

from sage.categories.category import Category
from sage.structure.parent import Parent
from sage.structure.element import Element

##############################################################################
# Examples that are displayed on the front page

EXAMPLES = [
    "Partition([3,3,2,1])",
    "Permutations(5)",
    "DihedralGroup(6)",
    "EllipticCurve('37b2')",
    "Crystals().example()",
    "HopfAlgebrasWithBasis(QQ).example()",
    ]

##############################################################################
# PropertyDisplayers for Elliptic curves

PropertyDisplayer(Parent,  "Object of", code = "category")
PropertyDisplayer(Element, "Element of", code = "parent")

from sage.categories.finite_enumerated_sets import FiniteEnumeratedSets
from sage.categories.finite_semigroups import FiniteSemigroups

PropertyDisplayer(FiniteEnumeratedSets(), "Cardinality");
PropertyDisplayer(lambda x: x in FiniteSemigroups() and x.cardinality() < 21, "Multiplication Table");
PropertyDisplayer(Category, "Example");

##############################################################################
# PropertyDisplayers for Elliptic curves

from sage.schemes.elliptic_curves.ell_number_field import EllipticCurve_number_field
from sage.schemes.elliptic_curves.ell_rational_field import EllipticCurve_rational_field

PropertyDisplayer(EllipticCurve_rational_field, "Torsion Points")
PropertyDisplayer(EllipticCurve_number_field, "Minimal Weierstrass equation", code = "global_minimal_model")
# Mordell-Weil group structure
# PropertyDisplayer("Mordell-Weil group structure", )
PropertyDisplayer(EllipticCurve_number_field, "Torsion generators",
          code = lambda E: E.torsion_subgroup().gens())
PropertyDisplayer(EllipticCurve_number_field, "Integral points")

# TODO: style information so that
# Note:
# We are taking here the decision that the conductor method is displayed in factored form
# Do we want to teach Sage that the conductor method is a "number theoretical method"
# and use that information so that, anywhere on the site, the result
# of computing a conductor method is always displayed in factored form
PropertyDisplayer(EllipticCurve_number_field, "N",      code = lambda E: E.conductor()   .factor(), section = "PropertyDisplayers",)
PropertyDisplayer(EllipticCurve_number_field, "\Delta", code = lambda E: E.discriminant().factor(), section = "PropertyDisplayers",)

# FIXME: reinstate once ReproducibleObject supports arguments to methods
#PropertyDisplayer(EllipticCurve_number_field, "N", code = lambda E: E.q_eigenform(10), section = ["Modular PropertyDisplayers","Modular form"])

# TODO: Instate this once Sage has a modular_degree method which would calculate and/or fetch the data from a database
#PropertyDisplayer(EllipticCurve_number_field, "Modular Degree", section = "PropertyDisplayers")

##############################################################################
# PropertyDisplayers for partitions

from sage.combinat.partition import Partition

PropertyDisplayer(Partition, "Conjugate")
PropertyDisplayer(Partition, "Hook lengths")
