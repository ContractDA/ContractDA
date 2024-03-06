from contractda.sets.set_base import SetBase
import random

class ExplicitSet(SetBase):
    """
    A set class that explicitly enumerate all elements
    """
    def __init__(self, vars: list[str], values: list[tuple]):
        """
        Constructor

        :param list[str] vars: The names for the variables
        :param list[tuple] values: The value in the set, each tuple is an element in the set, and the value in the tuple is the same order as that in the vars
        """
        # sort the variables
        var_arg_sorted = argsort(vars)
        self._var_order = var_arg_sorted
        self._vars: list[str] = [vars[i] for i in var_arg_sorted]
        self._values_internal = set([tuple([val_tuple[i] for i in var_arg_sorted]) for val_tuple in values]) #list[list] = self.__convert_values_to_internal(values)

    def __str__(self):
        return f"{tuple(self._vars)} = {str(self._values_internal)}"
    
    @property
    def internal_vars(self) -> list[str]:
        """
        The names for the variables, which is sorted
        """
        return self._vars

    @property
    def ordered_vars(self) -> list[str]:
        """
        The names for the variables, which is not sorted and may reflect the original input from designer
        """
        return [self._vars[id] for id in self._var_order]

    @property
    def internal_values(self) -> list[dict]:
        """
        The value of each element, each element is represented by a dictionary whose key are the variable name and value are the values for the variable
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
        # check the variables
        pass

    @staticmethod 
    def intersect(set1, set2):
        pass

    @staticmethod 
    def difference(set1, set2):
        pass

    @staticmethod 
    def complement(set1, set2):
        pass

    @staticmethod 
    def project(set1):
        pass

    def __iter__(self):
        self._iter = iter(self._values_internal) 
        return self

    def __next__(self):
        value = next(self._iter)
        return value

    def sample(self):
        random.seed(0)
        random_id = random.randrange(0, self.len())
        return list(self._values_internal)[random_id]

    def len(self):
        return len(self._vars)

    # def __convert_values_to_internal(self, vars: list[str], values: list[tuple]):
    #     internal = [[value[i] for value in values] for i, var in enumerate(vars)]

    #     return internal

    # def __convert_values_to_external(self, vars: list[str], values: dict[str, list]):  
    #     if not vars:
    #         return {}

    #     external_list = [ tuple([ for values[vars[i]]]) for i, value in enumerate(values[vars[0]])]

    #     return internal_dict

    # def __vars_conform(vars1, vars2):
    #     # return the variables after resolving the difference in order and names

    #     if set(vars1) == set(vars2)

def argsort(seq):
    # http://stackoverflow.com/questions/3071415/efficient-method-to-calculate-the-rank-vector-of-a-list-in-python
    return sorted(range(len(seq)), key=seq.__getitem__)