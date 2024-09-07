from __future__ import annotations
from typing import Iterable
import copy
from jsonschema import validate, ValidationError

from contractda.design._port import Port
from contractda.design._connections import Connection, ModuleConnection
from contractda.logger._logger import LOG
from contractda.design._system_contracts import SystemContract

class FrozenModuleExcpetion(Exception):
    pass

class Module(object):
    """A class that defines a system for reuse purpose"""
    def __init__(self, name: str, ports: Iterable[Port] | None = None, contracts: Iterable[SystemContract] | None = None):
        port_maps = dict() # maps something like d1.a d2.a to the same ports if d1 and d2 are of the same module but require different instance in the system.
        self._name: str = name
        self._submodules: dict[str, Module] = dict()
        # dictionary that maps instance name to the module, so the name can be different

        # instantiate the ports for the systems
        # if port_rename is None:
        #     port_rename = dict()
        self._ports: dict[str, Port] = dict()
        if ports is not None:
            self._ports = {port.port_name: port for port in ports}   
            for port in ports:
                port._set_system(self)   

        self._contracts: set[SystemContract] = {}
        if contracts is not None:
            self._contracts: set[SystemContract] = {contract for contract in contracts}

        self._connections: dict[str, ModuleConnection] = dict()
        self._frozen: bool = False

    # json schema
    schema = {
        "type": "object",
        "properties": {
            "module_name": {"type": "string"},
            "ports": {
                "type": "array",
                "items": Port._schema
            },
            "submodules": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "module": {"type": "string"},
                        "instance_name": {"type": "string"}
                    }
                }
            },
            "connections": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string"},
                        "terminals": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                }
            },
            "contracts": {
                "type": "array",
                "items": SystemContract.schema
            }

        },
        "required": ["module_name", "ports", "submodules", "connections", "contracts"]
    }

    def to_dict(self) -> dict:
        connections_obj = []
        
        for connection in self._connections.values():
            conn_obj = {"name": connection.name}
            conn_obj["terminals"] = list(connection.level_name_list)
            connections_obj.append(conn_obj)


        ret_dict = {
            "module_name": self._name,
            "ports": [port.to_dict() for port in self._ports.values()],
            "submodules": [{"module": module.name ,"instance_name": instance_name} for instance_name, module in self._submodules.items()],
            "connections": connections_obj,
            "contracts": [contract.to_dict() for contract in self._contracts]
        }
        return ret_dict
    
    @classmethod
    def from_dict(cls, dict_obj, modules:dict = None):
        try:
            validate(instance=dict_obj, schema=cls.schema)
        except ValidationError as e:
            LOG.error(f"System Definition Error", e)
            return None
        # reading system name
        module_name = dict_obj["module_name"]
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

        new_inst = cls(name=module_name, 
            ports = ports, 
            contracts = contracts)
        
        for port_name, port in new_inst.ports.items():
            port._set_system(new_inst)
        
        # reading subsystems
        subsystems = []
        submod_defs = dict_obj["submodules"]
        for submod_def in submod_defs: 
            module_name = submod_def["module"]
            instance_name = submod_def["instance_name"]
            module_ref = modules[module_name]
            new_inst.add_submodule(submodule=module_ref, instance_name=instance_name)

        # reading connections
        conn_defs = dict_obj["connections"]
        for conn_def in conn_defs:
            conn_name = conn_def["name"]
            terminals = []
            instance_names = []
            for term_name in conn_def["terminals"]:
                # parse terminal name
                tokens = term_name.split(".")
                if len(tokens) != 2:
                    LOG.error(f"Terminal name error! {term_name}, {len(term_name)}, {tokens}")
                instance_name = tokens[0]
                port_name = tokens[1]

                if instance_name == new_inst.module_name:
                    port = new_inst.ports[port_name]
                else:
                    port = new_inst.submodules[instance_name].ports[port_name]
                terminals.append(port)
                instance_names.append(instance_name)

            conn = ModuleConnection(name=conn_name, terminals=terminals, instance_names=instance_names)
            new_inst.add_connection(conn)

        return new_inst
    
    def set_ports(self):
        """Setting the ports """
        if self._check_is_frozen_before_modify():
            return 
        
        pass

    def set_contracts(self):
        """Setting the contracts"""
        if self._check_is_frozen_before_modify():
            return 
        pass

    def report(self) -> None:
        print(f"Module Report: {self._name} compile status: {self.is_frozen()}")
        print(f"  Ports: ")
        for port in self.ports.values():
            print(f"    {port}")
        print(f"  Subsystems: ")
        for instance_name, submodule in self.submodules.items():
            print(f"    {submodule.module_name} {instance_name}")
        print(f"  Contracts: ")
        for contract in self.contracts:
            print(f"    {contract}")
        print(f"  Connections: ")
        for connection in self.connections.values():
            print(f"    {connection}")       


    @property
    def name(self):
        return self._name
    
    @property
    def module_name(self):
        return self._name
    
    @property
    def submodules(self):
        return self._submodules
    
    @property
    def ports(self):
        return self._ports
    
    @property
    def contracts(self):
        return self._contracts
    
    @property
    def connections(self):
        return self._connections

    def add_submodule(self, submodule: Module, instance_name: str) -> None:
        if self._check_is_frozen_before_modify():
            return 
        if instance_name not in self._submodules:
            self._submodules[instance_name] = submodule
        else:
            LOG.error(f"Duplicated submodule instance name {instance_name}!")

    def add_connection(self, connection: ModuleConnection) -> None:
        if self._check_is_frozen_before_modify():
            return 
        if connection.name not in self._connections:
            # TODO: check if the connection terminals are all specify in this 
            self._connections[connection.name] = connection
            connection._set_system = self
        else:
            LOG.error(f"Duplicated connection {connection.name}!")

    def allow_modify(self):
        self._frozen = False

    def is_frozen(self):
        return self._frozen

    def _check_is_frozen_before_modify(self):
        if self.is_frozen():
            LOG.error(f"Module {self._name} is frozen! Please call Module.allow_modify() before modification.")
            raise FrozenModuleExcpetion(f"Module {self._name} is frozen! Please call Module.allow_modify() before modification.")
            return True
        else:
            return False