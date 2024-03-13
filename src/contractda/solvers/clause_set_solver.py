from __future__ import annotations
from typing import Iterable, Any

from contractda.solvers.solver_base import SolverBase
from contractda.vars._var import Var
from contractda.sets._clause import Clause


class ClauseSetSolver(SolverBase):
    """Solver for clause set
     A solver is a backend tool for reasoning the set expression, such as finding elements, checking subset, checking equivalence.

    The theory prover is the backend external tool for reasoning
    """

    def __init__(self, theory_prover = "z3"):
        pass

    def check_contain(self,  set_expr: Any, element: Any) -> bool:
        pass

    def check_subset(self, set_expr_a: Any, set_expr_b: Any) -> bool:
        pass

    def check_proper_subset(self, set_expr_a: Any, set_expr_b: Any) -> bool:
        pass

    def get_enumeration(self, set_expr: Any) -> Iterable:
        pass

    def check_satifiable(self, set_expr: Any) -> Any:
        
        pass

    def check_equivalence(self, set_expr_a: Any, set_expr_b: Any) -> bool:
        pass

    def check_disjoint(self, set_expr_a: Any, set_expr_b: Any) -> bool:
        pass

    def _encode(self, clause: Clause):
        root = clause.root
        
        #self._prover.

    def _encode(self, ast_node):
        pass


