
from typing import Iterable, TYPE_CHECKING
from jsonschema import validate, ValidationError

if TYPE_CHECKING:
    from contractda.design._system import System

from contractda.design._port import Port, PortDirection
from contractda.logger._logger import LOG

class Connection(object):
    """Connection between ports in a system"""
    def __init__(self, name: str, terminals: Iterable[Port]) -> None:
        """
        :param str name: the name of the connection
        :param Iterable[Port] terminals: the list of ports connected by the connection.
        """
        self._terminals = terminals
        self._name: str = name
        self._system: System = None
    
    def __str__(self) -> str:
        return f"{self._name} [" + ", ".join([term.level_name for term in self._terminals])+ "]"
            
    @property
    def terminals(self) -> Iterable[Port]:
        """The port (terminals) of the connections. It returns a list, where each element is a :py:class:`Port` instance"""
        return self._terminals
    
    @property
    def hier_name(self) -> str:
        """The hierarchical name in a design."""
        hier = [self._name]
        if self._system is not None:
            hier.append(self._system.hier_name)

        hier.reverse()
        return ".".join(hier)

    @property
    def name(self) -> str:
        """The name of the connection."""
        return self._name
    
    def report(self) -> None:
        """Report the information of the connection in the design view"""
        print(f"Connection Report: {self.hier_name}")
        for term in self.terminals:
            print(f"   {term.hier_name}")

    def _set_system(self, system: "System"):
        self._system = system

    @property
    def level_name_list(self) -> Iterable[str]:
        """The list of all level names of the terminals in the connection."""
        return [term.level_name for term in self._terminals]
    


class ModuleConnection(Connection):
    """Connection for module"""
    def __init__(self, name: str, terminals: Iterable[Port], instance_names: Iterable[str]) -> None:
        super().__init__(name=name, terminals=terminals)
        if not self._is_valid_instance_names(instance_names=instance_names):
            raise Exception("Number of terminals and instance names do not match")
        self._instance_names = instance_names # only use of module connection

    def _is_valid_instance_names(self, instance_names: Iterable[str]):
        return len(self.terminals) == len(instance_names)

    @property
    def instance_names(self) -> Iterable[str]:
        return self._instance_names

    def __str__(self) -> str:
        return f"{self._name} [" + ", ".join(self.level_name_list)+ "]"

    @property
    def level_name_list(self) -> Iterable[str]:
        return [term._level_name_by_instance_name(inst_name) for term, inst_name in zip(self._terminals, self._instance_names)]