from set_base import SetBase

class ExplicitSet(SetBase):
    def __init__(self, vars: list[str], values: list[tuple]):
        self.__vars: list[str] = vars
        self.__values_internal = values #list[list] = self.__convert_values_to_internal(values)

    def __str__(self):
        return f"{tuple(self.__vars)} = {str(self.__values_internal)}"
    
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
        self._iter = iter(self.__values) 
        return self

    def __next__(self):
        value = next(self._iter)
        return value


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

