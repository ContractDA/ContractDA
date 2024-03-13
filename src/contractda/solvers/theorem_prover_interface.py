from abc import ABC, abstractmethod, abstractstaticmethod
from typing import Callable


class TheoremSolverInterface(ABC):
    """Temporary not used, but should be able to insert into AST to create clause"""

    def __init__(self):
        pass

    @abstractstaticmethod
    def get_fresh_variable(var_name: str, sort: str, **kwargs):
        pass

    @abstractmethod
    def get_constant_value(self, sort: str, value, **kwargs):
        pass

    @abstractmethod
    def generate_clause_from_function(self, sym_clause_fn: Callable, vs: dict):
        """vs: the dictionary that contains map the name in the contract template to actual variables"""

    @abstractmethod
    def clause_implication(self, anticedent, consequent):
        """Note: this is used for setting component selection, but may be used to do in ast"""

    @abstractmethod
    def set_timeout(self, timeout_millisecond=100000):
        pass

    @abstractstaticmethod
    def clause_and(*args):
        pass

    @abstractstaticmethod
    def clause_or(*args):
        pass

    @abstractstaticmethod
    def clause_not(arg):
        pass

    @abstractstaticmethod
    def clause_equal(arg1, arg2):
        pass

    @abstractstaticmethod
    def clause_neq(arg1, arg2):
        pass

    @abstractstaticmethod
    def clause_ge(arg1, arg2):
        pass

    @abstractstaticmethod
    def clause_gt(arg1, arg2):
        pass

    @abstractstaticmethod
    def clause_le(arg1, arg2):
        pass

    @abstractstaticmethod
    def clause_lt(arg1, arg2):
        pass

    @abstractstaticmethod
    def clause_implies(arg1, arg2):
        pass

    @abstractmethod
    def add_conjunction_clause(self, *args):
        pass

    @abstractmethod
    def check(self) -> bool:
        pass

    @abstractmethod
    def get_model_for_var(self, var):
        pass
