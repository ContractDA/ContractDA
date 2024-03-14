from __future__ import annotations
from typing import Iterable, Callable
from abc import ABC, abstractmethod
import copy


from contractda.vars._var import Var
from contractda.sets._clause import Clause
import contractda.sets._fol_lan as fol_lan
from contractda.sets._parsers import fol_parser

from contractda.solvers._z3_interface import Z3Interface



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

    def get_symbols(self) -> dict:
        return self._symbols
    
    def clause_not(self):
        self._root = fol_lan.PropositionNodeUniOp("!", self._root)
        return self

    def clause_and(self, other):
        self._root = fol_lan.PropositionNodeBinOp("&&", self._root, other._root)
        return self

    def clause_or(self, other):
        self._root = fol_lan.PropositionNodeBinOp("||", self._root, other._root)
        return self

    def clause_implies(self, other):
        self._root = fol_lan.PropositionNodeBinOp("->", self._root, other._root)
        return self

    def clause_eq(self, other):
        self._root = fol_lan.PropositionNodeBinOp("==", self._root, other._root)
        return self

    def clasue_project(self, vars, is_refine = True):
        raise NotImplementedError()
    
    def evaluate(self, value_table):
        return self._root.evaluate(value_table=value_table)
    
    @staticmethod
    def _symbols_sync(symb1, symb2) -> dict:
        """Make the two ast use the same symbols node for the same variables"""
        pass

