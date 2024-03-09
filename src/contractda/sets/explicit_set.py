""" Class for ExplicitSet
"""
from __future__ import annotations
from typing import Iterable

from contractda.sets.set_base import SetBase
from contractda.sets.var import Var

from contractda.solvers.explicit_set_solver import ExplicitSetSolver, ExplicitSetVarType, ExplicitSetElementType, ExplicitSetExpressionType

import random
import copy
import itertools

class ExplicitSet(SetBase):
    """
    A set class that explicitly enumerate all elements

    For projection and intersection, extension variables are accepted and specialized treatment is performed to improve the performance
    For difference and union, extension variables are treated as plain projecction.

    Note: Complement, and projection with refinement or, extension variables. Domain is enumerated and thus the performance might not good.
    If you can write the set with clause, theory prover can be used to accelates the set computation.

    """
    def __init__(self, vars: ExplicitSetVarType, expr: ExplicitSetExpressionType):
        """
        Constructor

        :param list[str] vars: The ids for the variables
        :param list[tuple] expr: The expression of the set, the explicit set
         requires a explicit expression by a list of tuple, each tuple is an element in the set, and the value in the tuple is the same order as that in the vars
        """
        #TODO: check if the provided value in the element of the expr is within the range of the vars
        # check no duplicate variable in vars
        if not self._verify_unique_vars(vars):
            var_names = [var.id for var in vars]
            raise Exception(f"Duplicate variables are not allowed {var_names}")
        
        if not self._verify_finite_domain(vars):
            violated_var = [var for var in vars if not var.is_finite()]
            raise Exception(f"The created domain is not finite: Variables: {violated_var}")
        # sort the variables
        var_arg_sorted = argsort(vars)
        # _var_order: stores the information about how to restore the original variable order
        self._var_order = var_arg_sorted
        # _vars: the variable ordered by hash values
        self._vars: list[Var] = [vars[i] for i in var_arg_sorted]
        # _expr_internal: the set expr corresponding to the variables ordered by _vars
        self._expr_internal =  self._convert_expr_to_internal(expr) 
        
        # solver
        self._solver = ExplicitSetSolver()

    def __str__(self):
        return f"{tuple([str(var)for var in self.ordered_vars])} = {str(self.ordered_expr)}"

    def __iter__(self):
        self._iter = iter(self._expr_internal) 
        return self

    def __next__(self):
        element = next(self._iter)
        return self._convert_elem_to_external(element)
    
    def enumerate(self) -> Iterable[ExplicitSetElementType]:
        return self._solver.get_enumeration(self._expr_internal)
    
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
        return [self._vars[id] for id in self._var_order]

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

    def union(self, set2) -> ExplicitSet:
        """ Return the union of the two set

        Compute the union of the two explicit set
        Note: if the variable set is different, projection is used
        :param ExplicitSet set2: The set for difference
        """
        # check vars
        set1 = self

        var1_set = set(set1._vars)
        var2_set = set(set2._vars)
        all_vars = var1_set.union(var2_set)

        # projection to ensure the variables are the same
        if all_vars != var1_set:
            set1 = set1.project(list(all_vars))
        if all_vars != var2_set:
            set2 = set2.project(list(all_vars))

        # same variables
        # compute the set union
        new_expr = set1._expr_internal.union(set2._expr_internal)
        ret = ExplicitSet(vars = set1._vars, expr=new_expr)

        new_var = self.ordered_vars
        new_var += [var for var in set2.ordered_vars if var not in new_var]
        ret._reorder_vars(new_var)
        return ret


    def intersect(self, set2) -> ExplicitSet:
        """ Return the intersect of the two set

        Compute the intersect of the two explicit set
        """
        # check the variables
        set1 = self
        vars1 = set1._vars
        vars2 = set2._vars

        var_set1 = set(vars1)
        var_set2 = set(vars2)
        # special case 1, same variables set
        if var_set1 == var_set2:
            # no need to reorder as the they are sorted
            expr = set1._expr_internal.intersection(set2._expr_internal)
            return ExplicitSet(vars=vars1.copy(), expr=expr)
            pass

        # special case 2, one is contained by the other
        # TODO: accerate by exploiting the special case
        if var_set1.issubset(var_set1):
            pass
        if var_set2.issubset(var_set1):
            pass

        len1 = len(vars1)

        # get the intersection
        
        overlapped_vars = var_set1.intersection(var_set2)
        overlapped_vars_idx1 = [i for i, var in enumerate(vars1) if var in overlapped_vars]
        overlapped_vars_idx2 = [i for i, var in enumerate(vars2) if var in overlapped_vars]
        unique_vars_idx2 = [i for i, var in enumerate(vars2) if var not in overlapped_vars]

        vars2_unique = [var for var in vars2 if var not in overlapped_vars]
        # get the new variables
        vars = vars1.copy()
        vars.extend(vars2_unique)

        expr1 = set1._expr_internal
        expr2 = set2._expr_internal

        ret_expr = set()
        for elem1 in expr1:
            for elem2 in expr2:
                #TODO: should create a set of overlapped expr to filter out those not in the intersection 
                overlapped_expr1 = tuple([elem1[i] for i in overlapped_vars_idx1])
                overlapped_expr2 = tuple([elem2[i] for i in overlapped_vars_idx2])
                if overlapped_expr1 == overlapped_expr2:
                    # same core, form an element in intersection
                    elem_list = list(elem1) + [elem2[i] for i in unique_vars_idx2]
                    new_elem = tuple(elem_list)
                    ret_expr.add(new_elem)

        return ExplicitSet(vars = vars, expr=ret_expr)


    def difference(self, set2: ExplicitSet) -> ExplicitSet:
        """Return a new set that is the difference of the given set to the set2

        Note: if the variable set is different, projection is used
        :param ExplicitSet set2: The set for difference
        """
        # check vars
        set1 = self

        var1_set = set(set1._vars)
        var2_set = set(set2._vars)
        all_vars = var1_set.union(var2_set)

        # projection to ensure the variables are the same
        if all_vars != var1_set:
            set1 = set1.project(list(all_vars))
        if all_vars != var2_set:
            set2 = set2.project(list(all_vars))

        # same variables
        # compute the set difference
        new_expr = set1._expr_internal - set2._expr_internal
        ret = ExplicitSet(vars = set1._vars, expr=new_expr)

        new_var = self.ordered_vars
        new_var += [var for var in set2.ordered_vars if var not in new_var]
        ret._reorder_vars(new_var)
        return ret


    def complement(self) -> ExplicitSet:
        """ Return a new set that is the complement of the set
        """
        domain = self._domain()
        new_expr = [elem for elem in domain if elem not in self._expr_internal]  
        ret = ExplicitSet(vars=self._vars, expr=new_expr)
        return ret

    def project(self, new_vars: Iterable[Var], is_refine = False) -> ExplicitSet:
        """Project the set onto the new variables.
        The projection can be refinement or abstraction.
        Abstraction mean the projection back to the original space is larger than the original set
        Refinement mean the projectio back to the original space is smaller than the original set
        For example, given (CategoricalVar("x", range(1,3)), CategoricalVar("y", range(1,3)), CategoricalVar("z", range(1,3)) = [(1, 2, 1), (1, 2, 2), (1, 1, 1)]
        The refinement projection on to x, y is (CategoricalVar("x", range(1,3)), CategoricalVar("y", range(1,3)) = [(1, 2)]
        The abstraction projection on to x, y is (CategoricalVar("x", range(1,3)), CategoricalVar("y", range(1,3)) = [(1, 2), (1, 1)]

        :param Iterable[str] vars: The id of the new variables
        :param bool is_refine: whether the resulting set is a refinement or abstraction, refinement results in a smaller project (must allow any values in the )
        :return: The new set after projection
        """

        # find overleapped variables:
        overlapped_vars = [var for var in new_vars if var in self._vars]
        # project to the subset
        ret = self._project_subset(overlapped_vars, is_refine = is_refine)
        added_vars = [var for var in new_vars if var not in self._vars]
        if added_vars:
            ret = ret._project_extend(added_vars)
        ret._reorder_vars(new_vars)
        return ret
    
    def _project_subset(self, new_vars: Iterable[Var], is_refine = False):
        """
        Project the set onto the new variables.

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

    def sample(self):
        random.seed(0)
        random_id = random.randrange(0, self.len())
        return list(self._expr_internal)[random_id]

    def len(self):
        return len(self._vars)
    
    def _verify_unique_vars(self, vars: list[Var]) -> bool:
        ids = [var.get_id() for var in vars]
        return len(set(ids)) == len(ids)
    
    def _verify_finite_domain(self, vars: list[Var]) -> bool:
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