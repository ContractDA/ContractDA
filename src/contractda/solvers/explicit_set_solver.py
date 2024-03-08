from __future__ import annotations
from typing import Iterable, NewType

from contractda.solvers.solver_base import SolverBase, SetValueType
from contractda.sets.var import Var

ExplicitSetVarType = list[Var]
ExplicitSetValueType = Iterable[tuple]

class ExplicitSetSolver(SolverBase):
    """Solver for explicit set
     A solver is a backend tool for reasoning the set expression, such as finding elements, checking subset, checking equivalence.

     Though explicit set is simple and can be done directly on its internal set operations, we separate the class to make it clear that 
     the :py:class:`contractda.sets.explicit_set.ExplicitSet` provides only the operation internally, i.e., no information of the sets is provided.
     The solver provide an interface to query, check, and extract information inside a set object.
    """

    def __init__(self):
        pass

