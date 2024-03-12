from abc import ABC, abstractmethod
from contractda.vars._var import Var
from contractda.sets._fol_lan import AST_Node
from contractda.sets.parsers import fol_parser

ClauseSetVarType = list[Var]
ClauseSetElementType = tuple



class Clause(ABC):
    """Base Class for Clause
    
    A Clause is a description that express the set implicitly through a condition.

    Given an assignment of the values to the variables, the values is in the set if the condition evaluates to true.
    """

    def __init__(self, description: str, ctx: dict):
        pass


class FOLClause(Clause):
    """First order clause
    
    The structure of a first order clause is represented as a abstract syntax tree

    """
    def __init__(self, description: str, ctx: dict):
        self._root: AST_Node = fol_parser.parse(description, ctx)
        pass
        