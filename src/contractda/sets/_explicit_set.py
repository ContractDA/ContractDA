""" Class for ExplicitSet
"""
from __future__ import annotations
from typing import Iterable, Any

from contractda.sets._base import SetBase
from contractda.vars._var import Var
from contractda.logger._logger import LOG

import random
import copy
import itertools

ExplicitSetVarType = list[Var]
ExplicitSetElementType = tuple
ExplicitSetExpressionType = Iterable[ExplicitSetElementType]

class ExplicitSet(SetBase):
    """
    A set class that explicitly enumerate all elements

    For projection and intersection, extension variables are accepted and specialized treatment is performed to improve the performance
    For difference and union, extension variables are treated as plain projecction.

    Note: Complement, and projection with refinement or, extension variables. Domain is enumerated and thus the performance might not good.
    If you can write the set with clause, theory prover can be used to accelates the set computation.

    :param list[str] vars: The ids for the variables
    :param list[tuple] expr: The expression of the set, the explicit set
        requires a explicit expression by a list of tuple, each tuple is an element in the set, and the value in the tuple is the same order as that in the vars
    """
    def __init__(self, vars: ExplicitSetVarType, expr: ExplicitSetExpressionType):

        #TODO: check if the provided value in the element of the expr is within the range of the vars
        # check no duplicate variable in vars
        if not self._verify_unique_vars(vars):
            var_names = [var.id for var in vars]
            raise Exception(f"Duplicate variables are not allowed {var_names}")
        
        if not self._verify_finite_domain(vars):
            violated_var = [var for var in vars if not var.is_finite()]
            raise Exception(f"The created domain is not finite: Variables: {violated_var}")
        
        # check if the tuple is ok
        for elem in expr:
            self._verify_match_len_element(elem, len(vars))

        # sort the variables
        var_arg_sorted = argsort(vars)
        # _var_order: stores the information about how to restore the original variable order
        self._var_order = var_arg_sorted
        # _vars: the variable ordered by hash values
        self._vars: list[Var] = [vars[i] for i in var_arg_sorted]
        # _expr_internal: the set expr corresponding to the variables ordered by _vars
        self._expr_internal =  self._convert_expr_to_internal(expr) 

    def __str__(self):
        return f"{tuple([str(var)for var in self.ordered_vars])} = {str(self.ordered_expr)}"

    @property
    def vars(self) -> set[Var]:
        return self._vars
    
    @property
    def internal_vars(self) -> ExplicitSetVarType:
        """
        The ids for the variables, which is sorted
        """
        return self._vars

    @property
    def ordered_vars(self) -> ExplicitSetVarType:
        """
        The ids for the variables, which is not sorted and may reflect the original input from designer
        """
        sorted_pair = sorted(zip(self._var_order, self._vars), key=lambda x: x[0])
        return [val for _, val in sorted_pair]
        #return [self._vars[id] for id in self._var_order]

    @property
    def internal_expr(self) -> ExplicitSetExpressionType:
        """
        The expr of the set, followed the internal_vars
        """
        return self._expr_internal
    
    @property
    def ordered_expr(self) -> ExplicitSetExpressionType:
        """
        Return the expr ordered by the ordered_vars
        """
        return self._convert_expr_to_external(self.internal_expr)

    @property
    def get_element_dict(self) -> list[dict]:
        """Return the element in the form of dictionaries with keys being the variables and value being the values in each element.
        """
        return [{k: v for k, v in zip(self._vars, elem)} for elem in self._expr_internal]
    
    def reorder_vars(self, vars: list[Var]) -> None:
        """ Change the order of variables
        """
        # check vars is unique
        if not self._verify_unique_vars(vars):
            raise Exception("Reorder must be using the same set of variables")
        if set(vars) != set(self._vars):
            raise Exception("Reorder must be using the same set of variables")
        
        self._reorder_vars(vars)

    def _reorder_vars(self, vars: list[Var]) -> None:
        # assume the variables are checked to be the same as the self._vars and are unique
        self._var_order = argsort(vars)

    ######################
    #   Extraction
    ######################

    def __iter__(self):
        self._iter = iter(self._expr_internal) 
        return self

    def __next__(self):
        element = next(self._iter)
        return self._convert_elem_to_external(element)
    
    def get_enumeration(self) -> Iterable[ExplicitSetElementType]:
        """ Enumerate the set elements

        :return: An iterable object that can produce all elements
        :rtype: Iterable
        """
        return list(self._expr_internal)
    
    def sample(self):
        """ Sample an element in the set

        :return: any element that is in the set
        :rtype: Any
        """
        random.seed(0)
        random_id = random.randrange(0, self.len())
        return list(self._expr_internal)[random_id]
    ######################
    #   Set Operation
    ######################

    def union(self, other: ExplicitSet) -> ExplicitSet:
        """ Union opration on set

        Note: if the variable set is different, projection is used

        :param ExplicitSet other: the set to be union with this set
        :return: A new set which represents the union of the two set
        :rtype: ExplicitSet
        """
        # check vars
        set1, set2 = self._context_sync(self, other)

        # same variables
        # compute the set union
        new_expr = set1._expr_internal.union(set2._expr_internal)
        ret = ExplicitSet(vars = set1._vars, expr=new_expr)

        new_var = self.ordered_vars
        new_var += [var for var in other.ordered_vars if var not in new_var]
        ret._reorder_vars(new_var)
        return ret


    def intersect(self, other: ExplicitSet) -> ExplicitSet:
        """ Intersect opration on set

        :param ExplicitSet other: the set to be intersect with this set
        :return: A new set which represents the intersect of the two set
        :rtype: ExplicitSet
        """
        # check vars
        set1, set2 = self._context_sync(self, other)

        # same variables
        # compute the set intersect
        new_expr = set1._expr_internal.intersection(set2._expr_internal)
        ret = ExplicitSet(vars = set1._vars, expr=new_expr)

        new_var = self.ordered_vars
        new_var += [var for var in other.ordered_vars if var not in new_var]
        ret._reorder_vars(new_var)
        return ret


    def difference(self, other: ExplicitSet) -> ExplicitSet:
        """ Difference opration on set 

        :param ExplicitSet other: the set to be difference with this set
        :return: A new set which represents the difference of the two set
        :rtype: ExplicitSet
        """
        # check vars
        set1, set2 = self._context_sync(self, other)

        # same variables
        # compute the set difference
        new_expr = set1._expr_internal - set2._expr_internal
        ret = ExplicitSet(vars = set1._vars, expr=new_expr)

        new_var = self.ordered_vars
        new_var += [var for var in other.ordered_vars if var not in new_var]
        ret._reorder_vars(new_var)
        return ret


    def complement(self) -> ExplicitSet:
        """ Complement opration on set 

        :return: A new set which represents the Complement of the set
        :rtype: Explicitset
        """
        domain = self._domain()
        new_expr = [elem for elem in domain if elem not in self._expr_internal]  
        ret = ExplicitSet(vars=self._vars, expr=new_expr)
        return ret

    def project(self, new_vars: Iterable[Var], is_refine = False) -> ExplicitSet:
        """ Projection opration of set onto the new variables 

        The projection can be refinement or abstraction.
        Abstraction mean the projection back to the original space is larger than the original set
        Refinement mean the projectio back to the original space is smaller than the original set
        For example, given (CategoricalVar("x", range(1,3)), CategoricalVar("y", range(1,3)), CategoricalVar("z", range(1,3)) = [(1, 2, 1), (1, 2, 2), (1, 1, 1)]
        The refinement projection on to x, y is (CategoricalVar("x", range(1,3)), CategoricalVar("y", range(1,3)) = [(1, 2)]
        The abstraction projection on to x, y is (CategoricalVar("x", range(1,3)), CategoricalVar("y", range(1,3)) = [(1, 2), (1, 1)]

        :param Iterable[Var] vars: the list of variables to be the projection result.
        :param bool is_refine: whether the projection is to result in refinement or abstraction
        :return: A new set which represents the Projection of the set on the input variables
        :rtype: SetBase
        """
        LOG.debug(f"Projection of Set {[var.id for var in self.ordered_vars]}{self.ordered_expr} to variables {[var.id for var in new_vars]}")

        # find overleapped variables:
        overlapped_vars = [var for var in new_vars if var in self._vars]
        # project to the subset
        ret = self._project_subset(overlapped_vars, is_refine = is_refine)
        added_vars = [var for var in new_vars if var not in self._vars]
        if added_vars:
            ret = ret._project_extend(added_vars)
        ret._reorder_vars(new_vars)
        LOG.debug(f"Result: {[var.id for var in ret.ordered_vars]}{ret.ordered_expr}")
        return ret
    
    def _project_subset(self, new_vars: Iterable[Var], is_refine = False):
        """ Project the set onto the new variables.

        :param Iterable[str] vars: The id of the new variables, which must be a subset of the variables in the set
        :param bool is_refine: whether the resulting set is a refinement or abstraction, refinement results in a smaller project (must allow any values in the )
        """
        # assume vars are subset of self._vars
        new_vars_set = {var for var in new_vars}
        indices = [i for i, var in enumerate(self._vars) if var in new_vars_set]
        # abstraction:
        if not is_refine:
            remain_vars = [var for var in self._vars if var in new_vars_set]
            # collect all matching expr
            new_expr = {tuple([elem[i] for i in indices]) for elem in self._expr_internal}
            ret = ExplicitSet(vars = remain_vars, expr = new_expr)
            ret._reorder_vars(new_vars)
            return ret

        # refinement: need to check if all other expr is covered
        if is_refine:
            discarded_vars = [var for var in self._vars if var not in new_vars_set] 
            ret = self
            for var in discarded_vars:
                ret = ret._project_refine_one_variable(var)
            ret._reorder_vars(new_vars)
            return ret            

    def _project_refine_one_variable(self, var: Var):   
        discarded_idx =  self._vars.index(var)
        discarded_domain = set(var._value_range)
        new_vars = [v for v in self._vars if v != var]
        # create a dictionary: key: new_elem_candidate, elem: discarded value set
        refine_dict = dict()
        for elem in self._expr_internal:
            cand = tuple([elem[i] for i, val in enumerate(elem) if i != discarded_idx])
            discarded_value = elem[discarded_idx]
            if cand not in refine_dict:
                refine_dict[cand] = set([discarded_value])
            else:
                refine_dict[cand].add(discarded_value)

        new_expr = [cand for cand, covered_expr in refine_dict.items() if covered_expr == discarded_domain]
        ret = ExplicitSet(vars = new_vars, expr = new_expr)
        return ret


    def _project_extend(self, new_vars: Iterable[Var], is_refine = True):   
        """ Extend the variables with new_vars
        """
        new_domain = [var._value_range for var in new_vars]

        new_expr = []
        for elem in self._expr_internal:
            for extend_elem in itertools.product(*new_domain):
                new_expr.append(tuple(list(elem) + list(extend_elem)))

        return ExplicitSet(self._vars + new_vars, new_expr)
    
    
    def is_contain(self, element: ExplicitSetElementType) -> bool:
        """ Check if the set is contain the element

        :param ExplicitSetElementType element: the element to be checked if it is contained in the set
        :return: True if the element is in the set. False if not.
        :rtype: bool
        """
        self._verify_match_len_element(element, len(self.ordered_vars))
        # convert to internal
        element = self._convert_elem_to_internal(element)
        return element in self.internal_expr

    def is_subset(self, other: ExplicitSet) -> bool:
        """ Check if the set is a subset of the other set

        :param ExplicitSet other: the other set to be check if this set is a subset of it.
        :return: True if this set is a subset of the other set. False if not.
        :rtype: bool
        """
        set1, set2 = self._context_sync(self, other)

        return set1.internal_expr.issubset(set2.internal_expr)

    def is_proper_subset(self, other: ExplicitSet) -> bool:
        """ Check if the set is a proper subset of the other set

        :param ExplicitSet other: the other set to be check if this set is a proper subset of it.
        :return: True if this set is a proper subset of the other set. False if not.
        :rtype: bool
        """
        set1, set2 = self._context_sync(self, other)

        return set1.internal_expr < set2.internal_expr

    def is_satifiable(self) -> bool:
        """ Check if the set is satisfiable, i.e., not empty

        :return: True if this set is satisfiable. False if not.
        :rtype: bool
        """
        return bool(self.internal_expr)

    def is_equivalence(self, other: ExplicitSet) -> bool:
        """ Check if the set is equivalent to the other set

        :param ExplicitSet other: the other set to be check if this set is equivalent to it.
        :return: True if this set is equivalent to the other set. False if not.
        :rtype: bool
        """
        set1, set2 = self._context_sync(self, other)

        return set1.internal_expr == set2.internal_expr

    def is_disjoint(self, other: ExplicitSet) -> bool:
        """ Check if the set is disjoint to the other set

        :param ExplicitSet other: the other set to be check if this set is disjoint to it.
        :return: True if this set is disjoint to the other set. False if not.
        :rtype: bool
        """
        set1, set2 = self._context_sync(self, other)

        return set1.internal_expr.isdisjoint(set2.internal_expr)

    @classmethod
    def generate_variable_equivalence_constraint_set(cls, vars: list[Var]) -> ExplicitSet:
        expr = []
        for var in vars:
            acceptable_value = var.value_range
            acceptable_behavior = ExplicitSetElementType([acceptable_value]*len(vars))
            expr.append(acceptable_behavior)

        return cls(vars = vars, expr=expr)

    def len(self):
        return len(self._vars)
    
    @staticmethod
    def _context_sync(set1: ExplicitSet, set2:ExplicitSet):
        """Make to set at the same page by project their variable"""
        # check vars
        new_set1 = set1
        new_set2 = set2

        var1_set = set(set1._vars)
        var2_set = set(set2._vars)
        all_vars = var1_set.union(var2_set)

        # projection to ensure the variables are the same
        if all_vars != var1_set:
            new_set1 = set1.project(list(all_vars))
        if all_vars != var2_set:
            new_set2 = set2.project(list(all_vars))
        
        return new_set1, new_set2

    @staticmethod  
    def _verify_match_len_element(element: ExplicitSetElementType, length: int) -> bool:
        """Check if the tuple is ok"""
        if len(element) != length:
            raise Exception(f"The number of variables does not match the tuple set {len(element)} and {length}")
        else:
            return True
    
    @staticmethod    
    def _verify_finite_domain(vars: list[Var]) -> bool:
        return all([var.is_finite() for var in vars])

    def _convert_elem_to_external(self, elem: tuple) -> tuple:  
        sorted_pair = sorted(zip(self._var_order, elem), key=lambda x: x[0])
        return tuple([val for _, val in sorted_pair])

    def _convert_expr_to_external(self, expr: list[tuple]) -> list[tuple]:
        return {self._convert_elem_to_external(elem) for elem in expr}

    # elem in var_order: the elem should go to place 
    def _convert_elem_to_internal(self, elem: tuple) -> tuple:  
        return tuple([ elem[idx] for idx in self._var_order])
    
    def _convert_expr_to_internal(self, expr: list[tuple]) -> list[tuple]:  
        return {self._convert_elem_to_internal(elem) for elem in expr}

    def _domain(self):
        return itertools.product(*[var.value_range for var in self._vars])

def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=lambda i: seq[i].get_id())