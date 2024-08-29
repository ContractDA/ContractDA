
from typing import Iterable
from contractda.design._port import Port

class Connection():
    """Connection between ports in a system"""
    def __init__(self, name: str, terminals: Iterable[Port]) -> None:
        self._terminals = terminals
        self._name: str = name

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