from abc import ABC, abstractmethod
from enum import Enum
from typing import Iterable

# enum for support type

# TODO: create a FiniteSetVar to contain range and bool
# TODO: rename range_integer as range
class VarType(Enum):
    """ Enum for variable type

    All the supported types are listed.

    """

    INTEGER = 0,
    REAL = 1,
    BOOL = 2,
    CATEGORICAL = 3

    def __str__(self) -> str:
        return self.name

class Var(ABC):
    
    """
    Abstract Base class for variables in the set
    """

    def __init__(self, id: str, var_type: str): 
        self._id = id
        self._var_type = var_type

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(\"{self._id}\")"
    
    @abstractmethod
    def is_finite(self) -> bool:
        """ Return whether the domain of this variable is finite'

        :return: True is the domain is finite, False if the domain is not
        :rtype: bool
        """
        pass

    def get_id(self) -> str:
        """Return the identifier of the variable

        :return: The identifier of the variable.
        :rtype: str
        """
        return self._id
    
    @property 
    def id(self) -> str:
        """ The identifier of the variable

        :rtype: str
        """
        return self._id
    
    @id.setter
    def id(self, value):
        """Set the identifier of the variable"""
        self._id = value

    @property
    def type_str(self) -> str:
        """ The identifier of the type
        """
        return var_type_string_map[self._var_type]

        
        

class IntVar(Var):
    """Integer variable
    
    :param str id: The identifier of the variable 
    """
    def __init__(self, id: str):
        super().__init__(id, var_type=VarType.INTEGER)

    def is_finite(self) -> bool:
        return False
        
class RealVar(Var):
    """Real Valued variable
    
    :param str id: The identifier of the variable 
    """
    def __init__(self, id: str):
        super().__init__(id, var_type=VarType.REAL)

    def is_finite(self) -> bool:
        return False


class BoolVar(Var):
    """Variable of boolean value

    :param str id: The identifier of the variable
    """
    def __init__(self, id: str):
        super().__init__(id, var_type=VarType.BOOL)

    @property
    def value_range(self):
        """The available values for the variable

        :return: The list of all available values for the variable
        :rtype: Iterable
        """
        return [False, True]

    def is_finite(self):
        return True
    
class CategoricalVar(Var):
    """Variable of categorical value

    The categorical value can be any hashable values, such as string, integer, float.
    """
    def __init__(self, id: str, value_range:Iterable):
        """Constructor

        :param str id: the identifier of the variable
        :param Iterable value_range: the set of allowed categorical values
        """
        super().__init__(id, var_type=VarType.CATEGORICAL)
        self._value_range = value_range

    def is_finite(self) -> bool:
        return True
    
    @property
    def value_range(self):
        """The available values for the variable

        :return Iterable: The list of all available values for the variable
        :rtype: Iterable
        """
        return self._value_range

    def __str__(self) -> str:
        return f"{self.__class__.__name__}(\"{self._id}\") ({str(self._value_range)})"

def is_subtype(a, b) -> bool:
    """check if variable a is a subtype of b, i.e., any value of a can be accepted by b
    """
    #TODO:
    return NotImplementedError


def create_var(id: str, var_type: VarType, **kwargs):
    if var_type == VarType.INTEGER:
        return IntVar(id)
    elif var_type == VarType.REAL:
        return RealVar(id)
    elif var_type == VarType.BOOL:
        return BoolVar(id)
    elif var_type == VarType.CATEGORICAL:
        return CategoricalVar(id, value_range=kwargs["value_range"])
    else:
        raise Exception(f"create_var: Not supported variable types")