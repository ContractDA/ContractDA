from __future__ import annotations
from typing import Iterable
import copy

from contractda.contracts import ContractBase
from contractda.design._port import Port
from contractda.design._connections import Connection
from contractda.logger._logger import LOG

class Design():
    def __init__(self, name):
        """A design consists of systems in multiple levels
        Any operation in the design level will be reflected recursively to all the systems in the design
        """
        self._name 
        self._system = None # the actual system for this design
        self._spec = []
        self._obj = []

    schema = {
        "type": "object",
        "properties": {
            "system_name": {"type": "string"},
            "ports": {
                "type": "array",
                "items": Port.schema
            },
            "subsystems": {"type": "string"},
            "libsystems": {"type": "string"},
            "connections": {
                "type": "array",
                "items": Connection.schema
            },
            "contracts": {
                "type": "array",
                "items": {"type": "string"}
            }

        },
        "required": ["system_name"]
    }

    def set_specification(self):
        pass