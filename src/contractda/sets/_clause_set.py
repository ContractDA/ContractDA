""" Class for ClauseSet
"""
from __future__ import annotations
from typing import Iterable, Callable, Any

from contractda.sets._base import SetBase
from contractda.vars._var import Var
from contractda.sets._clause import Clause
import random
import copy
import itertools

ClauseSetVarType = list[Var]
ClauseSetElementType = tuple

class ClauseSet(SetBase):
    """ClauseSet

    A Clause set is a set that use clause to describe the condition of the set

    Threrefore the clause set should be able to generate the context 
    When context is needed, go through the list of symbols and then store the Var in the astnode
    When two clause are combined, rename by changing the astnode in the tree or reply on context when created
    """
    def __init__(self, vars: ClauseSetVarType, expr: str, ctx = None):
        self._expr = None
        self._vars = None
        pass

    @property
    def expr(self):
        """The clause body"""
        return self._expr

    @property
    def vars(self):
        """The variables"""
        return self._vars
    ######################
    #   Extraction
    ######################
    def __iter__(self):
        pass
    
    def __next__(self):
        pass

    def get_enumeration(self) -> Iterable:
        """ Enumerate the set elements

        :return: An iterable object that can produce all elements
        :rtype: Iterable
        """
        pass

    def sample(self) -> Any:
        """ Sample an element in the set

        :return: any element that is in the set
        :rtype: Any
        """
        pass

    ######################
    #   Set Operation
    ######################
    def union(self, other: ClauseSet) -> ClauseSet:
        """ Union opration on set

        :param ClauseSet other: the set to be union with this set
        :return: A new set which represents the union of the two set
        :rtype: ClauseSet
        """
        pass

    def intersect(self, other: ClauseSet) -> ClauseSet:
        """ Intersect opration on set

        :param ClauseSet other: the set to be intersect with this set
        :return: A new set which represents the intersect of the two set
        :rtype: ClauseSet
        """
        pass

    def difference(self, other: ClauseSet) -> ClauseSet:
        """ Difference opration on set 

        :param ClauseSet other: the set to be difference with this set
        :return: A new set which represents the difference of the two set
        :rtype: ClauseSet
        """
        pass

    def complement(self) -> ClauseSet:
        """ Complement opration on set 

        :return: A new set which represents the Complement of the set
        :rtype: ClauseSet
        """
        pass

    def project(self, vars, is_refine = True):
        """ Projection opration on set 

        :param vars: the list of variables to be the projection result.
        :param bool is_refine: whether the projection is to result in refinement or abstraction
        :return: A new set which represents the Projection of the set on the input variables
        :rtype: ClauseSet
        """
        pass

    def is_contain(self, element: Any) -> bool:
        """ Check if the set is contain the element

        :param element: the element to be checked if it is contained in the set
        :return: True if the element is in the set. False if not.
        :rtype: bool
        """
        pass

    def is_subset(self, other: ClauseSet) -> bool:
        """ Check if the set is a subset of the other set

        :param ClauseSet other: the other set to be check if this set is a subset of it.
        :return: True if this set is a subset of the other set. False if not.
        :rtype: bool
        """
        pass

    def is_proper_subset(self, other: ClauseSet) -> bool:
        """ Check if the set is a proper subset of the other set

        :param ClauseSet other: the other set to be check if this set is a proper subset of it.
        :return: True if this set is a proper subset of the other set. False if not.
        :rtype: bool
        """
        pass

    def is_satifiable(self) -> bool:
        """ Check if the set is satisfiable, i.e., not empty

        :return: True if this set is satisfiable. False if not.
        :rtype: bool
        """
        pass

    def is_equivalence(self, other: ClauseSet) -> bool:
        """ Check if the set is equivalent to the other set

        :param ClauseSet other: the other set to be check if this set is equivalent to it.
        :return: True if this set is equivalent to the other set. False if not.
        :rtype: bool
        """
        pass

    def is_disjoint(self, other: ClauseSet) -> bool:
        """ Check if the set is disjoint to the other set

        :param ClauseSet other: the other set to be check if this set is disjoint to it.
        :return: True if this set is disjoint to the other set. False if not.
        :rtype: bool
        """
        pass

    @classmethod
    def generate_variable_equivalence_constraint_set(cls, vars: list[Var]) -> ClauseSet:
        pass

    @classmethod
    def generate_var_val_equivalence_constraint_set(cls, var: Var, val) -> ClauseSet:
        pass

    @classmethod
    def generate_var_val_gt_constraint_set(cls, var: Var, val) -> ClauseSet:
        pass

    @classmethod
    def generate_var_val_lt_constraint_set(cls, var: Var, val) -> ClauseSet:
        pass

    @staticmethod
    def _combine_vars(a: list[Var], b: list[Var]) -> list[Var]:
        """ Combine the Vars, return a list of var which has no duplicated

        Raise an error when the there are two different vars with the same id
        """
        all_vars = set(a).union(set(b))
        if not __class__._verify_unique_vars(all_vars):
            raise Exception(f"Not unique veriable found in {all_vars}")
        return all_vars

    @staticmethod
    def _intersect_vars(a: list[Var], b: list[Var]) -> list[Var]:
        all_vars = set(a).union(set(b))
        if not __class__._verify_unique_vars(all_vars):
            raise Exception(f"Not unique veriable found in {all_vars}")
        return set(a).intersection(set(b))

    @staticmethod
    def _check_context(vars: ClauseSetVarType, expr: Clause):
        """Check if the context is correctly specified in vars

        True if everything is OK
        False if something goes wrong
        Also return the list of failing vars
        """
        symbols = set(expr.get_symbols())
        var_ids = set([var.id for var in vars])
        failed_list = list(symbols - var_ids)
        result = not bool(failed_list)
        return result, failed_list

    def _create_context(self, vars):
        context = {}
        for v in vars:
            pass