from enum import Enum
from jsonschema import validate, ValidationError
from typing import TYPE_CHECKING

from contractda.vars import VarType, Var, create_var
from contractda.logger._logger import LOG

if TYPE_CHECKING:
    from contractda.design._system import System

class PortDirection(Enum):
    """ Enum for port directions
    """
    INPUT = 0,
    OUTPUT = 1,
    INOUT = 2

    def __str__(self) -> str:
        return self.name

class Port(object):
    """A class for specifying the basic element that a system interact with external environment
    System, LibSystem, and Module all use this class for specifying the port.
    """
    def __init__(self, port_name: str, port_type: VarType | str, direction: PortDirection | str, **kwargs):
        """
        :param str port_name: the name of the port
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        self._port_name: str  = port_name

        if isinstance(port_type, str):
            port_type = VarType[port_type]

        self._port_type: VarType = port_type

        if isinstance(direction, str):
            direction = PortDirection[direction]
        self._dir: PortDirection = direction
        self._system: System = None

        self._var: Var = create_var(port_name, port_type, **kwargs) # do not use this, need context to avoid duplicate name

    def __str__(self) -> str:
        """
        """
        return f"{self._port_type.name} {self._dir.name} {self._port_name}"

    @staticmethod
    def _create_var_using_hier_name(port: "Port") -> Var:
        var = create_var(id=port.hier_name, var_type=port.port_type)
        port._var = var
        return var

    @property
    def level_name(self) -> str:
        """
        The name at the current level of system/module/library system.
        """
        hier = [self._port_name]
        if self._system is not None:
            hier.append(self._system.system_name)

        hier.reverse()
        return ".".join(hier)

    @property
    def hier_name(self) -> str:
        """
        The hierarchical name in a design.
        """
        hier = [self._port_name]
        if self._system is not None:
            hier.append(self._system.hier_name)

        hier.reverse()
        return ".".join(hier)

    @property 
    def port_name(self) -> str:
        """The name of the port"""
        return self._port_name
    
    @property
    def port_type(self) -> VarType:
        """The type of the port"""
        return self._port_type
    
    @property
    def direction(self) -> PortDirection:
        """The direction of the port"""
        return self._dir
    
    def _level_name_by_instance_name(self, instance_name:str) -> str:
        """
        Get a modified level name by using instance_name as the upper level name.
        """
        hier = [self._port_name]
        hier.append(instance_name)
        hier.reverse()
        return ".".join(hier)

    # json schema
    _schema = {
        "type": "object",
        "properties": {
            "port_name": {"type": "string"},
            "port_type": {"type": "string"},
            "direction": {"type": "string"}
        },
        "required": ["port_name", "port_type", "direction"]
    }

    def to_dict(self) -> dict:
        """
        Create a json formatted dictionary object for the ports.
        The object can be then written to json file and read in as a portable file.

        :return: the json formated dictionary.
        :rtype: dict

        """
        return {
            "port_name": self._port_name,
            "port_type": self._port_type.name,
            "direction": self._dir.name
        }
    
    @classmethod
    def from_dict(cls, dict_obj) -> "Port":
        """
        Create a port instance from the json formatted dictionary object.

        :param dict dict_obj: the json formatted dictionary object.
        :return: the :py:class:`Port` object defined by dict_obj.
        :rtype: Port

        """
        try:
            validate(instance=dict_obj, schema=cls._schema)
        except ValidationError as e:
            LOG.error(f"Port Definition Error {repr(e)}")
            return None
    
        return cls(port_name=dict_obj["port_name"], port_type=VarType[dict_obj["port_type"]], direction=PortDirection[dict_obj["direction"]])

    
    def report(self) -> None:
        """Report the information of the port in the design view"""
        print(f"Port Report: {self.hier_name}, Type: {self.port_type}, Direction: {self.direction}")

    def _set_system(self, system: "System"):
        if self._system is not None:
            LOG.error(f"System has been set for port {self}, {self._system.system_name}, {self._system.hier_name}")
            pass #TODO help prevent port being misused
        self._system = system



    
