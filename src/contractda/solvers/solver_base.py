from abc import ABC, abstractmethod
from typing import Any, Iterable

SetValueType = Any

class SolverBase(ABC):
    """Base class for Solver
    
    A solver is a backend tool for reasoning the set expression, such as finding elements, checking subset, checking equivalence.

    """

    def __init__(self):
        pass

    @abstractmethod
    def check_contain(self,  set_values: Any, value: Any) -> bool:
        pass

    @abstractmethod
    def check_subset(self, set_values_a: Any, set_values_b) -> bool:
        pass

    @abstractmethod
    def get_enumeration(self, set_values: Any) -> Iterable:
        pass

    @abstractmethod
    def get_satifiable(self, set_values: Any) -> Any:
        pass

    @abstractmethod
    def check_equivalence(self, set_values_a: Any, set_values_b: Any) -> bool:
        pass

    @abstractmethod
    def check_disjoint(self, set_values_a: Any, set_values_b: Any) -> bool:
        pass

