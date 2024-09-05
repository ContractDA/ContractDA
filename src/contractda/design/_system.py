from __future__ import annotations
from typing import Iterable
import copy
from jsonschema import validate, ValidationError

from contractda.design._port import Port
from contractda.design._connections import Connection
from contractda.logger._logger import LOG
from contractda.design._system_contracts import SystemContract
from contractda.design._libsystem import LibSystem

class FrozenSystemExcpetion(Exception):
    pass

class System(object):
    """A class that describes (Sub)systems in a designs.
    
    A system is a part of a design that can include ports and contracts specifying the system.
    System can be further decomposed into mutiple (sub)systems.
    The subsystems are also systems which can be reused in other designs for promoting reuse of components.
    """
    def __init__(self, 
                 system_name: str, 
                 lib_system: LibSystem = None, 
                 port_rename = None, 
                 ports: Iterable[Port] | None = None, 
                 contracts: Iterable[SystemContract] | None = None):
        """Test"""
        #self._check_parameters()

        self._system_name: str = system_name
        self._lib_system: LibSystem = lib_system
        self._subsystems: dict[str, System] = dict()

        # instantiate the ports for the systems
        # if port_rename is None:
        #     port_rename = dict()
        self._ports: dict[str, Port] = dict()
        if self._lib_system:
            for port_name, port in self._lib_system.ports.items():
                port_instance = copy.deepcopy(port)
                port._set_system(self)
                self._ports[port_name] = port_instance
        else:
            for port in ports:
                self._ports[port.port_name] = port
                port._set_system(self)

                # if port_name in port_rename:
                #     self._ports[port_name] = 
            
        
            
        # contracts from template # be careful for the port name changed
        self._contracts: set[SystemContract] = {}
        if contracts is not None:
            self._contracts: set[SystemContract] = {contract for contract in contracts}

        self._connections: dict[str, Connection] = dict()
        #TODO copy libsystem connections

        self._frozen: bool = False

    # json schema
    schema = {
        "type": "object",
        "properties": {
            "system_name": {"type": "string"},
            "ports": {
                "type": "array",
                "items": Port.schema
            },
            "subsystems": {
                "type": "array",
                "items": {
                    "$ref": "#"
                }
            },
            "libsystems": {"type": "string"},
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
        "required": ["system_name", "ports", "subsystems", "connections", "contracts"]
    }

    def to_dict(self) -> dict:
        connections_obj = []
        for connection in self._connections.values():
            conn_obj = {"name": connection.name}
            conn_obj["terminals"] = [term.level_name for term in connection.terminals]
            connections_obj.append(conn_obj)

        ret_dict = {
            "system_name": self._system_name,
            "ports": [port.to_dict() for port in self._ports.values()],
            "subsystems": [subsystem.to_dict() for subsystem in self._subsystems.values()],
            "connections": connections_obj,
            "contracts": [contract.to_dict() for contract in self._contracts]
        }
        if self._lib_system:
            ret_dict["lib_system"] = self._lib_system.name
        return ret_dict
    
    @classmethod
    def from_dict(cls, dict_obj, libs = None):
        try:
            validate(instance=dict_obj, schema=cls.schema)
        except ValidationError as e:
            LOG.error(f"System Definition Error", e)
            return None
        # reading system name
        system_name = dict_obj["system_name"]
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

        new_inst = cls(system_name=system_name, 
            lib_system = None,
            ports = ports, 
            contracts = contracts)
        
        for port_name, port in new_inst.ports.items():
            port._set_system(new_inst)
        
        # reading subsystems
        subsystems = []
        subsys_defs = dict_obj["subsystems"]
        for subsys_def in subsys_defs:
            new_inst.add_subsystem(System.from_dict(subsys_def))

        # reading connections
        conn_defs = dict_obj["connections"]
        for conn_def in conn_defs:
            conn_name = conn_def["name"]
            terminals = []
            for term_name in conn_def["terminals"]:
                # parse terminal name
                tokens = term_name.split(".")
                if len(tokens) != 2:
                    LOG.error(f"Terminal name error! {term_name}, {len(term_name)}, {tokens}")
                sys_name = tokens[0]
                port_name = tokens[1]

                if sys_name == system_name:
                    port = new_inst.ports[port_name]
                else:
                    port = new_inst.subsystems[sys_name].ports[port_name]
                terminals.append(port)

            conn = Connection(name=conn_name, terminals=terminals)
            new_inst.add_connection(conn)
            
        # reading libsystem
        if "lib_system" in dict_obj:
            libsystem = dict_obj["lib_system"]
            if libsystem not in libs:
                LOG.error(f"LibSystem {libsystem} not found!")
            
        
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

    def flatten(self):
        """Make the systems consist of only the lowest level subsystems"""
        raise NotImplementedError

    def allow_modify(self):
        self._frozen = False

    def is_frozen(self):
        return self._frozen
    
    def _check_is_frozen_before_modify(self):
        if self.is_frozen():
            LOG.error(f"System Instance {self.system_name} is frozen! Please call System.allow_modify() before modification.")
            raise FrozenSystemExcpetion(f"System Instance {self.system_name} is frozen! Please call System.allow_modify() before modification.")
            return True
        else:
            return False


    def _check_well_define(self):
        # 1. check connections connect through subsystem ports and self ports
        # 2. if there is subsystem, the system must be covered by subsystems (all ports are mapped)
        # 3. check output ports cannot connect to output ports

        # check ports
        pass

    def report(self) -> None:
        print(f"System Report: {self.system_name} compile status: {self.is_frozen()}")
        print(f"  Ports: ")
        for port in self.ports.values():
            print(f"    {port}")
        print(f"  Subsystems: ")
        for subsystem in self.subsystems.values():
            print(f"    {subsystem.system_name}")
        print(f"  Contracts: ")
        for contract in self.contracts:
            print(f"    {contract}")
        print(f"  Connections: ")
        for connection in self.connections.values():
            print(f"    {connection}")       


    @property
    def system_name(self):
        return self._system_name
    
    @property
    def lib_system(self) -> LibSystem | None:
        return self._lib_system
    
    @property
    def template_name(self) -> str:
        if self._lib_system:
            return self._lib_system.name
        else:
            return ""
    
    @property
    def subsystems(self):
        return self._subsystems
    
    @property
    def ports(self):
        return self._ports
    
    @property
    def contracts(self):
        return self._contracts
    
    @property
    def connections(self):
        return self._connections

    def add_subsystem(self, subsystem: System) -> None:
        if self._check_is_frozen_before_modify():
            return 
        if subsystem.system_name not in self._subsystems:
            self._subsystems[subsystem.system_name] = subsystem
        else:
            LOG.error(f"Duplicated subsystem {subsystem.system_name}!")

    def add_connection(self, connection: Connection) -> None:
        if self._check_is_frozen_before_modify():
            return 
        if connection.name not in self._connections:
            # TODO: check if the connection terminals are all specify in this 
            self._connections[connection.name] = connection
            connection._set_system = self
        else:
            LOG.error(f"Duplicated connection {connection.name}!")

class CompiledSystem(System):
    """A system that is fixed
    """
