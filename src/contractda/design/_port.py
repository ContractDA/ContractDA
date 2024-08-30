from enum import Enum
from jsonschema import validate, ValidationError

from contractda.vars import VarType, Var, create_var
from contractda.logger._logger import LOG

class PortDirection(Enum):
    """ Enum for port directions
    All the supported directions are listed.

    """
    INPUT = 0,
    OUTPUT = 1,
    INOUT = 2

    def __str__(self) -> str:
        return self.name

class Port(object):
    """A port is the basic element that a system interact with external environment"""
    def __init__(self, port_name: str, port_type: VarType | str, direction: PortDirection | str, **kwargs):
        self._port_name: str  = port_name

        if isinstance(port_type, str):
            port_type = VarType[port_type]

        self._port_type: VarType = port_type

        if isinstance(direction, str):
            direction = PortDirection[direction]
        self._dir: PortDirection = direction

        self._var: Var = create_var(port_name, port_type, **kwargs) # do not use this, need context to avoid duplicate name

    def __str__(self) -> str:
        return f"{self._port_type.name} {self._dir.name} {self._port_name}"

    # json schema
    schema = {
        "type": "object",
        "properties": {
            "port_name": {"type": "string"},
            "port_type": {"type": "string"},
            "direction": {"type": "string"}
        },
        "required": ["port_name", "port_type", "direction"]
    }

    def to_dict(self) -> dict:
        return {
            "port_name": self._port_name,
            "port_type": self._port_type.name,
            "direction": self._dir.name
        }
    
    @classmethod
    def from_dict(cls, dict_obj):
        try:
            validate(instance=dict_obj, schema=cls.schema)
        except ValidationError as e:
            LOG.error(f"Port Definition Error", e)
            return None
    
        return cls(port_name=dict_obj["port_name"], port_type=VarType[dict_obj["port_type"]], direction=PortDirection[dict_obj["direction"]])

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

    
