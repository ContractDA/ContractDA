from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Any, Iterable
from contractda.vars._var import Var



class SetBase(ABC):
    """
    Base class for different set objects
    """

    def __init__(self, solver):
        self._vars: Iterable[Var] = None
        pass
    
    @property
    def vars(self) -> Iterable[Var]:
        """The variables"""
        return self._vars
    ######################
    #   Extraction
    ######################
    @abstractmethod
    def __iter__(self):
        pass
    
    @abstractmethod
    def __next__(self):
        pass

    @abstractmethod
    def get_enumeration(self) -> Iterable:
        """ Enumerate the set elements

        :return: An iterable object that can produce all elements
        :rtype: Iterable
        """
        pass

    @abstractmethod
    def sample(self) -> Any:
        """ Sample an element in the set

        :return: any element that is in the set
        :rtype: Any
        """
        pass
    
    ######################
    #   Set Operation
    ######################
    @abstractmethod
    def union(self, other: SetBase) -> SetBase:
        """ Union opration on set

        :param SetBase other: the set to be union with this set
        :return: A new set which represents the union of the two set
        :rtype: SetBase
        """
        pass

    @abstractmethod
    def intersect(self, other: SetBase) -> SetBase:
        """ Intersect opration on set

        :param SetBase other: the set to be intersect with this set
        :return: A new set which represents the intersect of the two set
        :rtype: SetBase
        """
        pass

    @abstractmethod
    def difference(self, other: SetBase) -> SetBase:
        """ Difference opration on set 

        :param SetBase other: the set to be difference with this set
        :return: A new set which represents the difference of the two set
        :rtype: SetBase
        """
        pass

    @abstractmethod
    def complement(self) -> SetBase:
        """ Complement opration on set 

        :return: A new set which represents the Complement of the set
        :rtype: SetBase
        """
        pass

    @abstractmethod
    def project(self, vars, is_refine = True):
        """ Projection opration on set 

        :param vars: the list of variables to be the projection result.
        :param bool is_refine: whether the projection is to result in refinement or abstraction
        :return: A new set which represents the Projection of the set on the input variables
        :rtype: SetBase
        """
        pass

    @abstractmethod
    def is_contain(self, element: Any) -> bool:
        """ Check if the set is contain the element

        :param element: the element to be checked if it is contained in the set
        :return: True if the element is in the set. False if not.
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_subset(self, other: SetBase) -> bool:
        """ Check if the set is a subset of the other set

        :param SetBase other: the other set to be check if this set is a subset of it.
        :return: True if this set is a subset of the other set. False if not.
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_proper_subset(self, other: SetBase) -> bool:
        """ Check if the set is a proper subset of the other set

        :param SetBase other: the other set to be check if this set is a proper subset of it.
        :return: True if this set is a proper subset of the other set. False if not.
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_satifiable(self) -> bool:
        """ Check if the set is satisfiable, i.e., not empty

        :return: True if this set is satisfiable. False if not.
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_equivalence(self, other: SetBase) -> bool:
        """ Check if the set is equivalent to the other set

        :param SetBase other: the other set to be check if this set is equivalent to it.
        :return: True if this set is equivalent to the other set. False if not.
        :rtype: bool
        """
        pass

    @abstractmethod
    def is_disjoint(self, other: SetBase) -> bool:
        """ Check if the set is disjoint to the other set

        :param SetBase other: the other set to be check if this set is disjoint to it.
        :return: True if this set is disjoint to the other set. False if not.
        :rtype: bool
        """
        pass

    @classmethod
    def generate_variable_equivalence_constraint_set(cls, vars: list[Var]) -> "SetBase":
        """ Generate a set that force the variable to have the same values

        :param list[Var] vars: the variable that has the same values.
        :return: the set that force the variables to have the same values.
        :rtype: SetBase
        """
        pass

    @classmethod
    def generate_var_val_equivalence_constraint_set(cls, var: Var, val) -> "SetBase":
        """ Generate a set that force the variable to have the value

        :param Var vars: the variable that to set the value.
        :param val: the value for the variable
        :return: the set that force the variables to have the value.
        :rtype: SetBase
        """
        pass

    @staticmethod
    def _verify_unique_vars(vars: list[Var]) -> bool:
        ids = [var.get_id() for var in vars]
        return len(set(ids)) == len(ids)
