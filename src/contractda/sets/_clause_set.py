""" Class for ClauseSet
"""
from __future__ import annotations
from typing import Iterable, Callable

from contractda.sets._base import SetBase
from contractda.vars._var import Var
from contractda.sets._clause import Clause, ClauseSetVarType, ClauseSetElementType
import random
import copy
import itertools

class ClauseSet(SetBase):
    """ClauseSet

    A Clause set is a set that use clause to describe the condition of the set

    Threrefore the clause set should be able to generate the context 
    When context is needed, go through the list of symbols and then store the Var in the astnode
    When two clause are combined, rename by changing the astnode in the tree or reply on context when created
    """
    def __init__(self, vars: ClauseSetVarType, expr: str, ctx = None):
        pass

    def __iter__(self):
        pass
    
    def __next__(self):
        pass

    def sample(self):
        """
        Sample an element in the set
        """
        pass
    ######################
    #   Set Operation
    ######################
    def union(self, other):
        # make the variables in the same space
        pass

    def intersect(self, other):
        pass

    def difference(self, other):
        pass

    def complement(self):
        pass

    def project(self, vars, is_refine = True):
        pass

    def check_satifiable(self) -> bool:
        pass


    def _check_context(self, vars: ClauseSetVarType, expr: Clause):
        """Check if the context is correctly specified in vars

        True if everything is OK
        False if something goes wrong
        Also return the list of failing vars
        """
        symbols = set(expr.get_symbols().keys())
        var_ids = set([var.id for var in vars])
        failed_list = list(symbols - var_ids)
        result = not bool(failed_list)
        return result, failed_list

    def _create_context(self, vars):
        context = {}
        for v in vars:
            pass