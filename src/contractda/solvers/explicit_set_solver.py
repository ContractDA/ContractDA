from __future__ import annotations
from typing import Iterable, NewType

from contractda.solvers.solver_base import SolverBase, SetValueType
from contractda.sets.var import Var

ExplicitSetVarType = list[Var]
ExplicitSetElementType = tuple
ExplicitSetExpressionType = Iterable[ExplicitSetElementType]


class ExplicitSetSolver(SolverBase):
    """Solver for explicit set
     A solver is a backend tool for reasoning the set expression, such as finding elements, checking subset, checking equivalence.

     Though explicit set is simple and can be done directly on its internal set operations, we separate the class to make it clear that 
     the :py:class:`contractda.sets.explicit_set.ExplicitSet` provides only the operation internally, i.e., no information of the sets is provided.
     The solver provide an interface to query, check, and extract information inside a set object.
    """

    def __init__(self):
        pass

    def check_contain(self,  set_expr: ExplicitSetExpressionType, value: ExplicitSetElementType) -> bool:
        pass

    def check_proper_contain(self, set_expr_a: ExplicitSetExpressionType , set_expr_b: ExplicitSetExpressionType) -> bool:
        pass

    def check_subset(self, set_expr_a: ExplicitSetExpressionType , set_expr_b: ExplicitSetExpressionType) -> bool:
        pass

    def check_proper_subset(self, set_expr_a: ExplicitSetExpressionType , set_expr_b: ExplicitSetExpressionType) -> bool:
        pass

    def get_enumeration(self, set_expr: ExplicitSetExpressionType ) -> Iterable:
        pass

    def is_satifiable(self, set_expr: ExplicitSetExpressionType) -> bool:
        pass

    def check_equivalence(self, set_expr_a: ExplicitSetExpressionType, set_expr_b: ExplicitSetExpressionType ) -> bool:
        pass

    def check_disjoint(self, set_expr_a: ExplicitSetExpressionType, set_expr_b: ExplicitSetExpressionType ) -> bool:
        pass