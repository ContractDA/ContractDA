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
    """
    def __init__(self, vars: ClauseSetVarType, expr: str, clause_type: Callable):
        """ clause_type: the """
        # create the context
        self._expr = clause_type(description = expr)
        pass

    def union(self, set2):
        """Test
        """

    def _create_context(self, vars):
        context = {}
        for v in vars:
            pass