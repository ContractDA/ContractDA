from __future__ import annotations
from typing import Iterable

from contractda.solvers.solver_base import SolverBase
from contractda.sets.var import Var

ClauseSetVarType = list[Var]
ClauseValueType = None

class ClauseSetSolver(SolverBase):
    """Solver for clause set
     A solver is a backend tool for reasoning the set expression, such as finding elements, checking subset, checking equivalence.

    The theory prover is the backend external tool for reasoning
    """

    def __init__(self, theory_prover):
        pass