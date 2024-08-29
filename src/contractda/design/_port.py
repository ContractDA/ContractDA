
from contractda.vars import VarType, Var
from enum import Enum

class PortDirection(Enum):
    """ Enum for port directions
    All the supported directions are listed.

    """
    INPUT = 0,
    OUTPUT = 1,
    INOUT = 2

class Port():
    """A port is the basic element that a system interact with external environment"""
    def __init__(self, port_name: str, port_type: VarType | str, direction: PortDirection | str):
        self._port_name: str  = port_name

        if isinstance(port_type, str):
            port_type = VarType[port_type]

        self._port_type: VarType = port_type

        if isinstance(direction, str):
            direction = PortDirection[direction]
        self._dir: PortDirection = direction

        self._var: Var = None

    @property 
    def port_name(self) -> str:
        return self._port_name
    
    @property
    def port_type(self) -> VarType:
        return self._port_type
    
    @property
    def direction(self) -> PortDirection:
        return self._dir
    
    def report(self) -> None:
        print(f"Port Report: {self.port_name}, Type: {self.port_type}, Direction: {self.direction}")
