from __future__ import annotations
from typing import Iterable
import copy
from jsonschema import validate, ValidationError

from contractda.design._port import Port
from contractda.design._connections import Connection
from contractda.logger._logger import LOG
from contractda.design._system_contracts import SystemContract

class LibSystem(object):
    """A class that defines library system, which is a module without submodule"""
    def __init__(self, name: str, ports: Iterable[Port] | None = None, contracts: Iterable[SystemContract] | None = None):
        self._name: str = name

        self._ports: dict[str, Port] = dict()
        if ports is not None:
            self._ports = {port.port_name: port for port in ports}   
            for port in ports:
                port._set_system(self)   

        self._contracts: set[SystemContract] = {}
        if contracts is not None:
            self._contracts: set[SystemContract] = {contract for contract in contracts}

    schema = {
        "type": "object",
        "properties": {
            "lib_system_name": {"type": "string"},
            "ports": {
                "type": "array",
                "items": Port._schema
            },
            "contracts": {
                "type": "array",
                "items": SystemContract.schema
            }

        },
        "required": ["lib_system_name", "ports", "contracts"]
    }

    def to_dict(self) -> dict:
        ret_dict = {
            "lib_system_name": self._name,
            "ports": [port.to_dict() for port in self._ports.values()],
            "contracts": [contract.to_dict() for contract in self._contracts]
        }
        return ret_dict
    
    @classmethod
    def from_dict(cls, dict_obj):
        try:
            validate(instance=dict_obj, schema=cls.schema)
        except ValidationError as e:
            LOG.error(f"LibSystem Definition Error {repr(e)}")    
            return None
        # reading system name
        name = dict_obj["lib_system_name"]
        # reading ports
        ports = []
        port_defs = dict_obj["ports"]
        for port_def in port_defs:
            port = Port.from_dict(port_def)
            ports.append(port)

        # reading contracts
        contracts = []
        contract_defs = dict_obj["contracts"]
        for contract_def in contract_defs:
            contracts.append(SystemContract.from_dict(contract_def))

        new_inst = cls(name=name, 
            ports = ports, 
            contracts = contracts)
        
        return new_inst
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def ports(self) -> dict[str, Port]:
        return self._ports
    
    @property
    def contracts(self) -> set[SystemContract]:
        return self._contracts
    

    def add_port(self, port: Port) -> None:
        if self._check_is_frozen_before_modify():
            return 
        if port.port_name not in self._ports:
            self._ports[port.port_name] = port
            port._set_system(self)  
        else:
            LOG.error(f"Duplicated port name {port.port_name}!")
        
    def add_contract(self, contract) -> None:
        if self._check_is_frozen_before_modify():
            return 
        if contract not in self._contracts:
            self._contracts.add(contract)
        else:
            LOG.error(f"Duplicated contract {contract}!")

    def report(self) -> None:
        print(f"LibSystem Report: {self.name}")
        print(f"  Ports: ")
        for port in self.ports.values():
            print(f"    {port}")
        print(f"  Contracts: ")
        for contract in self.contracts:
            print(f"    {contract}")