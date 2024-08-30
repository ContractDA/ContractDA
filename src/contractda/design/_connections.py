
from typing import Iterable, TYPE_CHECKING
from jsonschema import validate, ValidationError

if TYPE_CHECKING:
    from contractda.design._system import System

from contractda.design._port import Port

class Connection(object):
    """Connection between ports in a system"""
    def __init__(self, name: str, terminals: Iterable[Port]) -> None:
        self._terminals = terminals
        self._name: str = name
        self._system: System = None

    def __str__(self) -> str:
        return f"{self._name} [" + ", ".join([term.level_name for term in self._terminals])+ "]"

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "terminals": {
                "type": "array",
                "items": {"type": "string"}
            }
        },
        "required": ["name", "terminals"]
    }

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "terminals": [term.port_name for term in self._terminals]
        }
    
    @classmethod
    def from_dict(cls, dict_obj):
        # connection should not be called from from_dict, it rely on ports
        pass

    def report(self) -> None:
        print(f"Connection Report: ")
        for terminal in self.terminals:
            print(f"   {terminal.port_name}")
            
    @property
    def terminals(self) -> Iterable[Port]:
        return self._terminals
    
    @property
    def name(self) -> str:
        return self._name
    
    def _set_system(self, system: "System"):
        self._system = system