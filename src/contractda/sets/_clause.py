from abc import ABC, abstractmethod
from contractda.vars._var import Var



class Clause(ABC):
    """Base Class for Clause
    
    A Clause is a description that express the set implicitly through a condition represented as AST.

    Given an assignment of the values to the variables, the values is in the set if the condition evaluates to true.
    """
    def __init__(self, description: str, ctx: dict):
        self._root = None
        pass
    
    @abstractmethod
    def get_symbols(self) -> dict:
        pass
    
    @abstractmethod
    def clause_not(self):
        pass

    @abstractmethod
    def clause_and(self, other):
        pass

    @abstractmethod
    def clause_or(self, other):
        pass

    @abstractmethod
    def clasue_project(self, vars, is_refine = True):
        pass

    @property
    def root(self):
        """Get the AST root node"""
        return self._root






def LTLClause(Clause):
    """Linear Temporal Logic clause
    
    The structure of a LTL is represented as a abstract syntax tree

    """
    def __init__(self, description: str, ctx: dict):
        pass
        