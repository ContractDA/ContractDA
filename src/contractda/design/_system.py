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
from contractda.design._design_exceptions import FeedbackLoopException


from contractda.contracts import ContractBase

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
    def input_ports(self) -> list[Port]:
        return [port for port in self._ports.values() if port.direction == PortDirection.INPUT]
    
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

    def check_connections(self):
        """Check if the connections of the system is defined without problem
        
        Return True if connection is ok
        """
        for connection in self.connections.values():
            ret = self._check_terminal_directions(connection=connection)
            if not ret:
                LOG.error(f"connection: {connection.hier_name}")
                return False
        return True
    
    def is_cascade(self) -> bool:
        """Check if the connection of the subsystem is cascade composition
            Parallel Composition is treated as a special case of cascade composition
        """
        subsystems_orders = self.subsystem_topologoical_sort()
        if subsystems_orders is not None:
            return True
        else:
            return False
        
    def is_feedback(self) -> bool:
        """Check if the connection of the subsystem is feedback composition"""
        return not self.is_cascade()  
    
    def is_parallel(self) -> bool:
        """Check if the connection of the subsystem is parallel composition"""
        # subsystem is parallel if no connection involves different subsystem
        # if there is a port that is not a input/output, it is treated as feedback
        if self.subsystem_contain_inout_ports() or self.contain_inout_ports():
            return False
        
        adj_list = self._build_adjacency_list()
        for sys, adj_sys in adj_list.items():
            if adj_sys:
                return False
        return True

    def contain_inout_ports(self) -> bool:
        """Check if there is inout port in the system"""
        for port in self._ports.values():
            if port.direction == PortDirection.INOUT:
                return True
            
    def subsystem_contain_inout_ports(self) -> bool:
        """Check if there is inout port in its subsystem"""
        for subsystem in self._subsystems.values():
            for port in subsystem.ports.values():
                if port.direction == PortDirection.INOUT:
                    return True
                
    def subsystem_topologoical_sort(self) -> list[System] | None:
        """perform topological sort of the subsystem, return None if it cannot be sorted(contain loop)"""
        # build graph
        adj_list = self._build_adjacency_list()
        # system itself are ignored
        topological_order: list[System] = []
        unmarked_subsystem = set(self._subsystems.values())
        for subsystem in unmarked_subsystem:
            subsystem._ts_mark = 0 #0: unmarked 1: temporary 2: permanant
        while unmarked_subsystem:
            for sys in unmarked_subsystem:
                try:
                    self._subsystems_topological_sort_visit(sys, unmarked_subsystem, topological_order, adj_list)
                except FeedbackLoopException as e:
                    return None # loop detected
                break
        return topological_order

    def _subsystems_topological_sort_visit(self, sys: System, unmarked_subsystem: set[System], topological_order: list[System], adj_list: dict[System, set[System]]):
        if sys._ts_mark == 2:
            # reach an end that already sort 
            return
        if sys._ts_mark == 1:
            raise FeedbackLoopException("Loop detected during visit")
        
        sys._ts_mark = 1
        # collect all next subsystem
        for adj_subystem in adj_list[sys]:
            self._subsystems_topological_sort_visit(adj_subystem, unmarked_subsystem, topological_order, adj_list)

        sys._ts_mark = 2
        unmarked_subsystem.remove(sys)
        topological_order.append(sys)
        return 

#################### Connection Helper
    def _build_adjacency_list(self) -> dict[System, set[System]]:
        adj_list: dict[System, set[System]] = dict()
        for subsystem in self.subsystems.values():
            adj_list[subsystem] = set()
        for connection in self.connections.values():
            driver_term = self._get_connection_driver(connection=connection)
            driver_system = driver_term._system
            if driver_system == self:
                continue
            adj_terms: list[Port] = self._get_connection_sinks(connection=connection)
            adj_systems = {term._system for term in adj_terms if term._system != self}
            adj_list[driver_system].update(adj_systems)
        return adj_list
    
    def _connection_contain_(self, connection: Connection) -> bool:
        for term in connection.terminals():
            if term.system == self:
                return True
        return False
#################### contracts API
    def _convert_system_contract_to_contract_object(self):
        # match ports 
        # in contract we use the port name, but in system view we should use hierarchical name
        self.__vars = self._create_vars_for_port()
        self.__vars_remap = self._create_var_rename_for_hier_name()
        for contract in self.contracts:
            contract.convert_to_contract_object(self.__vars, self.__vars_remap)
        return
    
    def _get_single_system_contract(self) -> ContractBase:
        single_contract = None
        all_contracts = list(self.contracts)
        if len(all_contracts) >= 1:
            single_contract: ContractBase = all_contracts[0].contract_obj
        for contract in all_contracts[1:]:
            single_contract = single_contract.conjunction(contract.contract_obj)
        
        return single_contract


    def _get_subsystem_contract_composition(self) -> ContractBase:
        composed_contract = None
        all_contracts = [subsystem._get_single_system_contract() for subsystem in self.subsystems.values()]
        if None in all_contracts:
            return None # has a subsystem without contract, unable to define contract composition, missing contracts...

        if len(all_contracts) >= 1:
            composed_contract = all_contracts[0]
        for contract in all_contracts[1:]:
            composed_contract = composed_contract.composition(contract)
        
        return composed_contract
        # 

    def _get_contract_language_type(self):
        # return the first contract type
        for contract in self.contracts:
            break
        return type(contract._contract_obj.environment)
        
    
    def _generate_contract_system_connection_constraint(self, required_language = None):
        """Generate equivalence constraint for the connected ports including system ports"""
        # required_language: FOLClauseSet, (Set-like class) that implements equivalent set.
        #if required_language is none, it is set to the first contract type
        constraints = []
        if required_language is None:
            required_language = self._get_contract_language_type()
        for connection in self.connections.values():
            vars = [term._var for term in connection.terminals]
            constraints.append(required_language.generate_variable_equivalence_constraint_set(vars=vars))
            
        if len(constraints) > 0:
            aggregate_constraints = constraints[0]
            for constraint in constraints:
                aggregate_constraints = aggregate_constraints.intersect(constraint)

            return aggregate_constraints
        else:
            return None

    def _create_vars_for_port(self) -> list[Var]:
        return [Port._create_var_using_hier_name(port=port) for port in self.ports.values()]
    
    def _get_port_var_map(self) -> dict[Port, Var]:
            return {port: port.var for port in self._ports.values()}
    
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
        
    def _get_connection_driver(self, connection: Connection) -> Port:
        """Return a driver of the connection, assume the connection has only one driver"""
        for term in connection.terminals:
            if term in self._ports.values():
                if term.direction == PortDirection.INPUT:
                    return term
            else:
                if term.direction == PortDirection.OUTPUT:
                    return term
        raise Exception("No driver found")

    
    def _get_connection_sinks(self, connection: Connection) -> Iterable[Port]:
        """Return a sinks of the connection"""
        sinks = []
        for term in connection.terminals:
            if term in self._ports.values():
                if term.direction != PortDirection.INPUT:
                    sinks.append(term)
            else:
                if term.direction != PortDirection.OUTPUT:
                    sinks.append(term)
        return sinks
        
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

class CompiledSystem(System):
    """A system that is fixed
    """
