from abc import ABC, abstractmethod
from typing import Any, Iterable

SetValueType = Any

class SolverBase(ABC):
    """Base class for Solver
    
    A solver is a backend tool for reasoning the set expression, such as finding elements, checking subset, checking equivalence.
    Its purpose is to provide elements and answer yes-no question regarding the set, thus requiring reasoning on the set objects
    The solver should assume the variables are well-maintained such that no concerns about order.
    The type of the internal data is also determined by the solver
    """

    def __init__(self):
        pass

    @abstractmethod
    def check_contain(self,  set_expr: Any, element: Any) -> bool:
        pass

    @abstractmethod
    def check_proper_contain(self, set_expr_a: Any, set_expr_b: Any) -> bool:
        pass

    @abstractmethod
    def check_subset(self, set_expr_a: Any, set_expr_b: Any) -> bool:
        pass

    @abstractmethod
    def check_proper_subset(self, set_expr_a: Any, set_expr_b: Any) -> bool:
        pass

    @abstractmethod
    def get_enumeration(self, set_expr: Any) -> Iterable:
        pass

    @abstractmethod
    def is_satifiable(self, set_expr: Any) -> Any:
        pass

    @abstractmethod
    def check_equivalence(self, set_expr_a: Any, set_expr_b: Any) -> bool:
        pass

    @abstractmethod
    def check_disjoint(self, set_expr_a: Any, set_expr_b: Any) -> bool:
        pass

