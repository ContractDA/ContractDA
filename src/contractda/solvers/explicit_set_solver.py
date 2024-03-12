from __future__ import annotations
from typing import Iterable, NewType

from contractda.solvers.solver_base import SolverBase, SetValueType
from contractda.vars._var import Var
from contractda.sets._explicit_set_def import ExplicitSetVarType, ExplicitSetElementType, ExplicitSetExpressionType
from functools import cmp_to_key

class ExplicitSetSolver(SolverBase):
    """Solver for explicit set
     A solver is a backend tool for reasoning the set expression, such as finding elements, checking subset, checking equivalence.

     Though explicit set is simple and can be done directly on its internal set operations, we separate the class to make it clear that 
     the :py:class:`contractda.sets.explicit_set.ExplicitSet` provides only the operation internally, i.e., no information of the sets is provided.
     The solver provide an interface to query, check, and extract information inside a set object.
    """

    def __init__(self):
        pass

    def check_contain(self,  set_expr: ExplicitSetExpressionType, element: ExplicitSetElementType) -> bool:
        """Check if the element is contained in the set represented by the expr

        :param ExplicitSetExpressionType set_expr: the expr that represents the set.
        :param ExplicitSetElementType element: the element to test if it is in the set.
        :return bool: True if the element is contained in the set
        """
        return element in set_expr

    def check_subset(self, set_expr_a: ExplicitSetExpressionType , set_expr_b: ExplicitSetExpressionType) -> bool:
        """Check if set_expr_a is a subset of set_expr

        :param ExplicitSetExpressionType set_expr_a: the expr that represents the set_a.
        :param ExplicitSetExpressionType set_expr_b: the expr that represents the set_b.
        :return bool: True if the set a is a subset of set b
        """
        return set_expr_a.issubset(set_expr_b)

    def check_proper_subset(self, set_expr_a: ExplicitSetExpressionType , set_expr_b: ExplicitSetExpressionType) -> bool:
        """Check if set_expr_a is a proper subset of set_expr

        :param ExplicitSetExpressionType set_expr_a: the expr that represents the set_a.
        :param ExplicitSetExpressionType set_expr_b: the expr that represents the set_b.
        :return bool: True if the set a is a proper subset of set b
        """
        return set_expr_a < set_expr_b

    def get_enumeration(self, set_expr: ExplicitSetExpressionType ) -> Iterable:
        """Return all elements in the set

        :param ExplicitSetExpressionType set_expr: the expr that represents the set.
        :return Iterable: the list of all elements
        """
        elements = list(set_expr)
        elements.sort()
        return elements

    def check_satifiable(self, set_expr: ExplicitSetExpressionType) -> bool:
        """Check if there is any element satisfying the set

        :param ExplicitSetExpressionType set_expr: the expr that represents the set.
        :return bool: true if there is satisfying element
        """
        return bool(set_expr)

    def check_equivalence(self, set_expr_a: ExplicitSetExpressionType, set_expr_b: ExplicitSetExpressionType ) -> bool:
        """Check if the two set represented by set_expr_a and set_expr_b are equivalent

        :param ExplicitSetExpressionType set_expr_a: the expr that represents the set_a.
        :param ExplicitSetExpressionType set_expr_b: the expr that represents the set_b.
        :return bool: True if the sets are equivalent
        """
        return set_expr_a == set_expr_b

    def check_disjoint(self, set_expr_a: ExplicitSetExpressionType, set_expr_b: ExplicitSetExpressionType ) -> bool:
        """Check if the two set represented by set_expr_a and set_expr_b are disjoint

        :param ExplicitSetExpressionType set_expr_a: the expr that represents the set_a.
        :param ExplicitSetExpressionType set_expr_b: the expr that represents the set_b.
        :return bool: True if the sets are disjoint
        """
        return set_expr_a.isdisjoint(set_expr_b)



