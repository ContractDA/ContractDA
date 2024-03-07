from contractda.sets.set_base import SetBase
from contractda.sets.var import Var
import random
import copy

class ExplicitSet(SetBase):
    """
    A set class that explicitly enumerate all elements
    """
    def __init__(self, vars: list[Var], values: list[tuple]):
        """
        Constructor

        :param list[str] vars: The ids for the variables
        :param list[tuple] values: The value in the set, each tuple is an element in the set, and the value in the tuple is the same order as that in the vars
        """
        # check no duplicate variable in vars
        if not self._verify_unique_vars(vars):
            var_names = [var.id for var in vars]
            raise Exception(f"Duplicate variables are not allowed {var_names}")
        # sort the variables
        var_arg_sorted = argsort(vars)
        # _var_order: stores the information about how to restore the original variable order
        self._var_order = var_arg_sorted
        # _vars: the variable ordered by hash values
        self._vars: list[Var] = [vars[i] for i in var_arg_sorted]
        # _values_internal: the set values corresponding to the variables ordered by _vars
        self._values_internal =  self._convert_values_to_internal(values) 

    def __str__(self):
        return f"{tuple([str(var)for var in self._vars])} = {str(self._values_internal)}"

    def __iter__(self):
        self._iter = iter(self._values_internal) 
        return self

    def __next__(self):
        value = next(self._iter)
        return value
    
    @property
    def internal_vars(self) -> list[str]:
        """
        The ids for the variables, which is sorted
        """
        return self._vars

    @property
    def ordered_vars(self) -> list[str]:
        """
        The ids for the variables, which is not sorted and may reflect the original input from designer
        """
        return [self._vars[id] for id in self._var_order]

    @property
    def internal_values(self) -> list[dict]:
        """
        The value of each element, each element is represented by a dictionary whose key are the variable id and value are the values for the variable
        """
        return [{k: v for k, v in zip(self._vars, elem)} for elem in self._values_internal]
    
    @property
    def ordered_values(self) -> list[tuple]:
        """
        Return the values ordered by the ordered_vars
        """
        return [tuple([ elem[id] for id in self._var_order]) for elem in self._values_internal]

    @staticmethod 
    def union(set1, set2):
        # union does not work if the sets have different variables




        pass

    def union(set2):
        pass

    @staticmethod 
    def intersect(set1, set2):
        """ Return the intersect of the two set

        Compute the intersect of the two explicit set
        """
        # check the variables
        vars1 = set1._vars
        vars2 = set2._vars

        var_set1 = set(vars1)
        var_set2 = set(vars2)
        # special case 1, same variables set
        if var_set1 == var_set2:
            # no need to reorder as the they are sorted
            values = set1._values_internal.intersection(set2._values_internal)
            return ExplicitSet(vars=vars1.copy(), values=values)
            pass

        # special case 2, one is contained by the other
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

        values1 = set1._values_internal
        values2 = set2._values_internal

        ret_values = set()
        for value1 in values1:
            for value2 in values2:
                overlapped_values1 = tuple([value1[i] for i in overlapped_vars_idx1])
                overlapped_values2 = tuple([value2[i] for i in overlapped_vars_idx2])
                if overlapped_values1 == overlapped_values2:
                    # same core, form an element in intersection
                    value_list = list(value1) + [value2[i] for i in unique_vars_idx2]
                    new_value = tuple(value_list)
                    ret_values.add(new_value)

        return ExplicitSet(vars = vars, values=ret_values)

    @staticmethod 
    def difference(set1, set2):
        pass

    @staticmethod 
    def complement(set1, set2):
        pass

    @staticmethod 
    def project(set1, vars, is_refine = True):
        """
        Project the set onto the new variables.
        For explicit set, new variables cannot be included as they cannot be represented in finite elements.

        :param list[str] vars: The id of the new variables
        :param bool is_refine: whether the resulting set is a refinement or abstraction, refinement results in a smaller project (must allow any values in the )
        """
        pass

    def sample(self):
        random.seed(0)
        random_id = random.randrange(0, self.len())
        return list(self._values_internal)[random_id]

    def len(self):
        return len(self._vars)
    
    def _verify_unique_vars(self, vars: list[Var]) -> bool:
        ids = [var.get_id() for var in vars]
        return len(set(ids)) == len(ids)

    def _convert_value_to_external(self, value: tuple) -> tuple:  
        sorted_pair = sorted(zip(self._var_order, value), key=lambda x: x[0])
        return tuple([val for _, val in sorted_pair])

    def _convert_values_to_external(self, values: list[tuple]) -> list[tuple]:
        return {self._convert_value_to_external(value) for value in values}

    # value in var_order: the value should go to place 
    def _convert_value_to_internal(self, value: tuple) -> tuple:  
        return tuple([ value[idx] for idx in self._var_order])
    
    def _convert_values_to_internal(self, values: list[tuple]) -> list[tuple]:  
        return {self._convert_value_to_internal(value) for value in values}

def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=lambda i: seq[i].get_id())