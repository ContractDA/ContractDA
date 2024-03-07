from abc import ABC, abstractmethod
from enum import Enum

# enum for support type
class VarType(Enum):
    """ Enum for variable type

    All the supported types are listed.

    """

    INTEGER = 0,
    REAL = 1,
    BOOL = 2,
    RANGE_INTEGER = 3

var_type_string_map = {VarType.INTEGER: "integer", VarType.REAL: "real", VarType.BOOL: "bool", VarType.RANGE_INTEGER: "range_integer"}

class Var(ABC):
    """
    Base class for variables

    Currently support integer, real, bool, and range
    """
    def __init__(self, id: str, var_type: str): 
        self._id = id
        self._var_type = var_type

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(\"{self._id}\")"
    
    @abstractmethod
    def is_finite(self):
        """ Return whether the domain of this variable is finite'

        :return: True is the domain is finite, False if the domain is not
        :rtype: bool
        """
        pass

    def get_id(self):
        return self._id
    
    @property 
    def id(self):
        return self._id

        
        

class IntVar(Var):
    def __init__(self, id: str):
        super().__init__(id, var_type=VarType.INTEGER)

    def is_finite(self) -> bool:
        return False
        
class RealVar(Var):
    def __init__(self, id: str):
        super().__init__(id, var_type=VarType.REAL)

    def _is_finite(self) -> bool:
        return False


class BoolVar(Var):
    def __init__(self, id: str):
        super().__init__(id, var_type=VarType.BOOL)

    def is_finite(self):
        return True
    
class RangeIntVar(Var):
    def __init__(self, id: str, value_range:range):
        super().__init__(id, var_type=VarType.RANGE_INTEGER)
        self._value_range = value_range

    def is_finite(self) -> bool:
        return True
    
    @property
    def value_range(self):
        return self._value_range

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(\"{self._id}\") ({str(self._value_range)})"

     