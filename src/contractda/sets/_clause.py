from abc import ABC, abstractmethod
from contractda.vars._var import Var
import contractda.sets._fol_lan as fol_lan
from contractda.sets.parsers import fol_parser

import copy

ClauseSetVarType = list[Var]
ClauseSetElementType = tuple



class Clause(ABC):
    """Base Class for Clause
    
    A Clause is a description that express the set implicitly through a condition represented as AST.

    Given an assignment of the values to the variables, the values is in the set if the condition evaluates to true.
    """
    def __init__(self, description: str, ctx: dict):
        self._root = None
        pass
    
    @abstractmethod
    def __copy__(self) :
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


class FOLClause(Clause):
    """First order clause
    
    The structure of a first order clause is represented as a abstract syntax tree

    """
    def __init__(self, description: str, ctx: dict):
        self._root: fol_lan.AST_Node = fol_parser.parse(description, ctx)
        self._symbols: dict = self._root.get_symbols()

    @classmethod
    def parse_clause(cls, description: str, ctx = None):
        root: fol_lan.AST_Node = fol_parser.parse(description, ctx)
        symbols: dict = root.get_symbols()
        return cls(root = root, symbols=symbols)

    def __copy__(self) :
        """ Shallow copy"""
        cls = self.__class__
        result = cls.__new__(cls)
        result._root = copy.deepcopy(self._root)
        result._symbols = result._root.get_symbols()
        return result
        

    def get_symbols(self) -> dict:
        return self._symbols
    
    def clause_not(self):
        self._root = fol_lan.PropositionNodeUniOp("!", self._root)

    def clause_and(self, other):
        self._root = fol_lan.PropositionNodeBinOp("&&", self._root, other._root)

    def clause_or(self, other):
        self._root = fol_lan.PropositionNodeBinOp("||", self._root, other._root)

    def clasue_project(self, vars, is_refine = True):
        raise NotImplementedError()
    
    @staticmethod
    def _symbols_sync(symb1, symb2) -> dict:
        """Make the two ast use the same symbols node for the same variables"""
        pass



def LTLClause(Clause):
    """Linear Temporal Logic clause
    
    The structure of a LTL is represented as a abstract syntax tree

    """
    def __init__(self, description: str, ctx: dict):
        pass
        