from __future__ import annotations
from typing import Iterable, TYPE_CHECKING
import copy
from jsonschema import validate, ValidationError

from contractda.design._port import Port, PortDirection
from contractda.design._connections import Connection
from contractda.logger._logger import LOG
from contractda.design._system_contracts import SystemContract, ContractType
from contractda.design._libsystem import LibSystem

from contractda.sets._fol_clause import FOLClause
from contractda.sets import FOLClauseSet
from contractda.sets._fol_lan import name_remap
from contractda.vars import Var

# from contractda.contracts import AGContract, CBContract

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
        """
        :param str system_name: the name of the system
        :param LibSystem lib_system: the reference library system for creating the system, when this parameter is set, the ports and contracts follow the library system and the inputs to these two parameters are ignored.
        :param Iterable[Port] ports: the list of ports for the system.
        :param Iterable[SystemContract]: the contracts for specifying the system.
        """
        #self._check_parameters()

        self._system_name: str = system_name
        self._lib_system: LibSystem = lib_system
        self._subsystems: dict[str, System] = dict()
        self._upsystem: System = None
        self._hier_name: str = None

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

    @property
    def system_name(self):
        """The name of the system"""
        return self._system_name
    
    @property
    def lib_system(self) -> LibSystem | None:
        """The library that the system is referenced to"""
        return self._lib_system
    
    @property
    def template_name(self) -> str:
        """The name of the library that the system is referenced to"""
        if self._lib_system:
            return self._lib_system.name
        else:
            return ""
    
    @property
    def subsystems(self) -> dict[str, System]:
        """The subsystems in the system. It returns a dictionary object, where the key is the subsystem names and the value is the subsystem :py:class:`System` instance"""
        return self._subsystems
    
    @property
    def ports(self) -> dict[str, Port]:
        """The ports in the system. It returns a dictionary object, where the key is the port names and the value is :py:class:`Port` instance"""
        return self._ports
    
    @property
    def contracts(self) -> set[SystemContract]:
        """The contracts in the system. It returns a python set object, where each element is a :py:class:`SystemContract` instance"""
        return self._contracts
    
    @property
    def connections(self) -> dict[str, Connection]:
        """The connections in the system. It returns a dictionary object, where the key is the connection names and the value is :py:class:`Connection` instance"""
        return self._connections
    
    @property
    def hier_name(self) -> str:
        """The hierarchical name in a design."""
        return self._hier_name
    
    # json schema
    _schema = {
        "type": "object",
        "properties": {
            "system_name": {"type": "string"},
            "ports": {
                "type": "array",
                "items": Port._schema
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
        """
        Create a json formatted dictionary object for the whole systems, including the contained subsystems.
        The object can be then written to json file and read in as a portable file.

        :return: the json formated dictionary.
        :rtype: dict
        """
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
    def from_dict(cls, dict_obj: dict, libs = None) -> System:
        """
        Create a system instance from the json formatted dictionary object.

        :param dict dict_obj: the json formatted dictionary object.
        :return: the :py:class:`System` object defined by dict_obj.
        :rtype: Port

        """
        try:
            validate(instance=dict_obj, schema=cls._schema)
        except ValidationError as e:
            LOG.error(f"System Definition Error {repr(e)}")            
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
    

    def report(self) -> None:
        """Report the information of the port in the design view"""
        print(f"System Report: {self.hier_name} compile status: {self.is_frozen()}")
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


    def add_subsystem(self, subsystem: System) -> None:
        """Add a subsystem to the system.
        
        :param System subsystem: the subsystem to be added to the system
        """
        if self._check_is_frozen_before_modify():
            return 
        if subsystem.system_name not in self._subsystems:
            self._subsystems[subsystem.system_name] = subsystem
            subsystem._upsystem = self
        else:
            LOG.error(f"Duplicated subsystem {subsystem.system_name}!")

    def add_connection(self, connection: Connection) -> None:
        """Add a connection to the system.
        The terminals in the connections must be the ports that has already existed in the system or its immediate subsystem.

        :param Connection connection: the connection to be added to the system
        """
        if self._check_is_frozen_before_modify():
            return 
        if connection.name not in self._connections:
            # TODO: check if the connection terminals are all specify in this 
            self._connections[connection.name] = connection
            connection._set_system = self
        else:
            LOG.error(f"Duplicated connection {connection.name}!")


#################### contracts API
    def _convert_system_contract_to_contract_object(self):
        # match ports 
        # in contract we use the port name, but in system view we should use hierarchical name
        vars = self._create_vars_for_port()
        vars_remap = self._create_var_rename_for_hier_name()
        for contract in self.contracts:
            contract.convert_to_contract_object(vars, vars_remap)
        return

    def _get_subsystem_contract_composition(self, subsystems: Iterable[System]):
        pass
        # 
    
    def _generate_contract_system_connection_constraint(self, required_language):
        """Generate equivalence constraint for the connected ports including system ports"""
        # required_language: FOLClauseSet, (Set-like class) that implements equivalent set.
        for connection in self.connections:
            pass



    def _create_vars_for_port(self) -> list[Var]:
        return [Port._create_var_using_hier_name(port=port) for port in self.ports.values()]
    
    def _create_var_rename_for_hier_name(self) -> dict[str, str]:
        return {port.port_name: port.hier_name for port in self.ports.values()}

    def _set_hier_name(self, hier_name:str):
        if self._hier_name is None:
            self._hier_name = hier_name
        else:
            LOG.error(f"Hier name has been set {self.system_name} {self.hier_name}")

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

    def check_connections(self):
        for connection in self.connections.values():
            ret = self._check_terminal_directions(connection=connection)
            if not ret:
                LOG.error(f"connection: {connection.hier_name}")
                return False
        

    def _check_terminal_directions(self, connection: Connection) -> bool:
        # check if multiple outputs drive the same coonnection, or no outputs
        must_drive_ports = []
        must_sink_ports = []
        flex_ports = []
        for term in connection.terminals:
            if term in self._ports.values():
                # might be optimized using better search
                if term.direction == PortDirection.OUTPUT:
                    must_sink_ports.append(term)
                elif term.direction == PortDirection.INPUT:
                    must_drive_ports.append(term)
                elif term.direction == PortDirection.INOUT:
                    flex_ports.append(term)
                else:
                    LOG.error(f"Unknown direction type {term.direction}")
                    return False
            else:
                if term.direction == PortDirection.OUTPUT:
                    must_drive_ports.append(term)
                elif term.direction == PortDirection.INPUT:
                    must_sink_ports.append(term)
                elif term.direction == PortDirection.INOUT:
                    flex_ports.append(term)
                else:
                    LOG.error(f"Unknown direction type {term.direction}")
                    return False

        if len(must_drive_ports) > 1:
            LOG.error(f"Multiple drives for connection {connection.name} ({[term.hier_name for term in must_drive_ports]})")
            return False
        if len(must_drive_ports) == 0 and len(flex_ports) == 0:
            LOG.error(f"No drives for connection {connection.name}")
            return False    
        
        return True

    def _check_feedback_loop(self):
        """Find the feedback loop in the subsystem connection"""
        # create a map that tells where the ports go:
        for port in self.ports.values():
            if port.port_type == PortDirection.INPUT:
                pass
        pass
class CompiledSystem(System):
    """A system that is fixed
    """
