""" Class for ClauseSet
"""
from __future__ import annotations
from typing import Iterable, Callable

from contractda.sets._base import SetBase
from contractda.vars._var import Var
from contractda.sets._clause import Clause, ClauseSetVarType, ClauseSetElementType
from contractda.solvers.clause_set_solver import ClauseSetSolver
from contractda.solvers._fol_clause_set_solver import FOLClauseSetSolver
import random
import copy
import itertools

class ClauseSet(SetBase):
    """ClauseSet

    Threrefore the clause set should be able to generate the context 
    When context is needed, go through the list of symbols and then store the Var in the astnode
    When two clause are combined, rename by changing the astnode in the tree or reply on context when created
    """
    def __init__(self, vars: ClauseSetVarType, expr: str, clause_type: type[Clause], ctx = None):
        """ clause_type: the """
        # create the context
        self._expr: Clause = clause_type(description = expr, ctx = ctx)
        # check if the variables are indeed mentioned in expr
        context_ok, failed_list = self._check_context(vars = vars, expr=self._expr)
        if not context_ok:
            failed_id = [var.get_id() for var in failed_list]
            raise Exception(f"Variables {failed_id} not specified in the description: {expr}")
        # store the 
        self._vars = vars
        # generate context
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
        solver = FOLClauseSetSolver()
        if solver.check_satifiable(vars=self._vars, set_expr=self._expr):
            print("Success")
        else:
            print("Fail")


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