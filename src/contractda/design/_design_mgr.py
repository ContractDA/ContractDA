
from contractda.design._system import System, Port, Connection, SystemContract
from contractda.logger._logger import LOG
from contractda.design._design_exceptions import IncompleteContractException, ObjectNotFoundException
import json

class DesignLevelManager():
    """The manager for all objects and the interface to perform system level task
    Mapping of names uses hierarchical names to avoid conflicts.
    """
    def __init__(self):
        self._systems = dict()
        self._ports = dict()
        self._connections = dict()
        self._modules = dict()
        self._libs = dict()

        self._designs: dict[str, System] = dict()# the entry to the top level systems


    def read_design_json(self, json_obj):
        """Read the design from a json file"""
        system = System.from_dict(json_obj, self)
        if system.system_name in self._designs:
            LOG.error(f"Design name {system.system_name} already existed! Reading aborted!")
            return 
        self.register_design(system=system)

    def export_design_json(self, system: str | System):
        """Write the design to a json file"""

    def read_design_from_file(self, file_path):
        # check file format
        # if format_is_json(file_path)
            with open(file_path, "r") as design_file:
                json_obj = json.load(design_file)
                self.read_design_json(json_obj)
        
    def check_system(self, system: str | System):
        raise NotImplementedError
        pass

    def verify_design(self, system: str | System):
        """Verify if the design has any potential issues
        This function encapsulate many verification problems and summarize the result.
        """
        raise NotImplementedError
        pass
    

    def verify_system(self, system: str | System):
        """Verify if the design has any potential issues
        This function encapsulate many verification problems and summarize the result.
        """
        raise NotImplementedError
        pass

    def verify_design_refinement(self, design: str | System, hierarchical=True) -> list[System]:
        """Verify if the given design satisfy refinement relation, hierarchical mean if the relation need to checked hierarchically"""
        system_obj = self._verify_design_obj_or_str(design=design)
        self._generate_system_contracts(system_obj)
        systems_under_test = [system_obj]
        failed_systems: list[System] = []
        while systems_under_test:
            test_system = systems_under_test.pop()
            try:
                is_refinement = self.verify_system_refinement(test_system)
                if not is_refinement:
                    failed_systems.append(test_system)
            except IncompleteContractException:
                continue
            systems_under_test.extend(list(test_system.subsystems.values()))
        return failed_systems

    def verify_system_refinement(self, system: str | System, hierarchical=True) -> bool:
        """Verify if the given design satisfy refinement relation, hierarchical mean if the relation need to checked hierarchically"""
        system_obj = self._verify_system_obj_or_str(system=system)
        self._generate_system_contracts(system_obj)
        system_contract = system_obj._get_single_system_contract()
        subsystem_composed_contract = system_obj._get_subsystem_contract_composition()
        if subsystem_composed_contract is None:
            raise IncompleteContractException("Subsystem does not have a complete contract defined for verifying refinement")
        connection_constraint = system_obj._generate_contract_system_connection_constraint()

        #connection constraint has to be put into everywhere for A, G, C, B for all contracts...
        system_contract.add_constraint(connection_constraint)
        subsystem_composed_contract.add_constraint(connection_constraint)
        return system_contract.is_refined_by(subsystem_composed_contract)



    def verify_design_independent(self, design: str | System, hierarchical=True) -> list[System]:
        """Verify if the given design may suffer from incompatible problems during independent design process"""
        if isinstance(system, str):
            system = self.get_design(system)
        if system is None:
            LOG.error(f"No such design, verification fails")
            return 
        raise NotImplementedError
        
    def verify_system_independent(self, system: str | System, hierarchical=True) -> bool:
        """Verify if the given design satisfy refinement relation, hierarchical mean if the relation need to checked hierarchically"""
        system_obj = self._verify_system_obj_or_str(system=system)
        
        # to verify independent design in system
        # 1. detect feedback loop
        # 2. bottom up: find leaf systems and check if they are receptive
        # 3. propagate leaf system up for pure refinement
        # 4. detect loop: composition of receptive does not guarantee to be receptive
        # 3. color up all those systems up that can be ensured to be receptive
        # 2. if feedback loop does not exist, check if receptive can be established -> should be done bottom up?
        # 2. For feedback loop, check feedback condition
        # 3. For system not involve in feedback loop, try to estabilish its receptiveness. check strong replaceability
        # 4. check receptiveness in the leaf
        # 5. 
        system_obj = self._verify_system_obj_or_str(system=system)
        is_cascade = False
        if is_cascade:
            # check receptiveness
            pass
        if len(system_obj.subsystems.values()) == 2:
            # simple case
            pass
        self._generate_system_contracts(system_obj)
        system_contract = system_obj._get_single_system_contract()
        connection_constraint = system_obj._generate_contract_system_connection_constraint()
        system_contract.add_constraint(connection_constraint)
        
        raise NotImplementedError

    def verify_design_consistensy(self, design: str | System, hierarchical=True) -> dict[System, list[SystemContract]]:
        """Check if the system contracts in a design are consistent

        :param str | System system: the system instance or its name for checking contract consistency
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        system_obj = self._verify_design_obj_or_str(design=design)
        systems_under_test = [system_obj]
        failed_contracts: dict[System, list[SystemContract]] = {}
        while systems_under_test:
            test_system = systems_under_test.pop()
            inconsistent_contracts = self.verify_system_consistensy(test_system)
            if inconsistent_contracts:
                failed_contracts[test_system] = inconsistent_contracts
            
            systems_under_test.extend(list(test_system.subsystems.values()))
        return failed_contracts

        pass

    def verify_system_consistensy(self, system: str | System, hierarchical=True) -> list[SystemContract]:
        """Check if the system contracts in a system are consistent

        :param str | System system: the system instance or its name for checking contract consistency
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        system_obj = self._verify_system_obj_or_str(system=system)
        self._generate_system_contracts(system_obj)
        inconsistent_contracts = []
        for contract in system_obj.contracts:
            if not contract.contract_obj.is_consistent():
                inconsistent_contracts.append(contract)
        return inconsistent_contracts
        


    def verify_design_compatibility(self, design: str | System, hierarchical=True) -> dict[System, list[SystemContract]]:
        """Check if the system contracts in a design are compatible

        :param str | System system: the system instance or its name for checking contract consistency
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        system_obj = self._verify_design_obj_or_str(design=design)
        systems_under_test = [system_obj]
        failed_contracts: dict[System, list[SystemContract]] = {}
        while systems_under_test:
            test_system = systems_under_test.pop()
            incompatible_contracts = self.verify_system_compatibility(test_system)
            if incompatible_contracts:
                failed_contracts[test_system] = incompatible_contracts
            
            systems_under_test.extend(list(test_system.subsystems.values()))
        return failed_contracts

    def verify_system_compatibility(self, system: str | System, hierarchical=True) -> list[SystemContract]:
        """Check if the system contracts in a system are consistent

        :param str | System system: the system instance or its name for checking contract consistency
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        system_obj = self._verify_system_obj_or_str(system=system)
        self._generate_system_contracts(system_obj)
        incompatible_contracts = []
        for contract in system_obj.contracts:
            if not contract.contract_obj.is_compatible():
                incompatible_contracts.append(contract)
        return incompatible_contracts



    def verify_design_connection(self, design: str | System, hierarchical=True):
        """Check if the system connection is well-defined

        :param str | System system: the system instance or its name for checking contract consistency
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        system_obj = self._verify_design_obj_or_str(design=design)
        systems_under_test = [system_obj]
        failed_systems: list[System] = []
        while systems_under_test:
            test_system = systems_under_test.pop()
            ret = self.verify_system_connection(test_system)
            if not ret:
                failed_systems.append(test_system)
            
            systems_under_test.extend(list(test_system.subsystems.values()))
        return failed_systems
    
    def verify_system_connection(self, system: str | System, hierarchical=True) -> list[SystemContract]:
        """Check if the system connection is well-defined

        :param str | System system: the system instance or its name for checking contract consistency
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        system_obj = self._verify_system_obj_or_str(system=system)
        ret = system_obj.check_connections()
        return ret


    def synthesize_systems(self):
        raise NotImplementedError
        pass

    def simulate_design(self, system: str | System, simulator):
        raise NotImplementedError
        pass

    def simulate_system(self, system: str | System, simulator):
        raise NotImplementedError
        pass


    def register_design(self, system: System):
        """Puts the systems, ports, and connections in the manager
        Recursively put them in the manager for every subsystem
        """
        tmp_sys: dict = dict() 
        tmp_ports:  dict = dict() 
        tmp_connections:  dict = dict() 
        hier_names = []
        self._designs[system.system_name] = system

        self._register_system(system, tmp_sys, tmp_ports, tmp_connections, hier_names)

        try:
            self._systems.update(tmp_sys)
            self._ports.update(tmp_ports)
            self._connections.update(tmp_connections)
        except Exception:
            LOG.error("Unknown error when registering systems.")

        return 

    @staticmethod
    def _register_system(system: System, tmp_sys, tmp_ports, tmp_connections, hier_names):
        # systems
        LOG.debug(f"Registering system {system.system_name}")
        

        hier_names_level = list(hier_names)
        hier_names_level.append(system.system_name)
        
        tmp_sys[_build_hier_name(hier_names_level)] = system
        system._set_hier_name(_build_hier_name(hier_names_level))
        # ports
        for port in system.ports.values():
            hier_names_port = hier_names_level + [port.port_name]
            tmp_ports[_build_hier_name(hier_names_port)] = port
        # connection
        for connection in system.connections.values():
            hier_names_conn = hier_names_level + [connection.name]
            tmp_connections[_build_hier_name(hier_names_conn)] = connection

        # recursive for subsystems
        for subsystem in system.subsystems.values():
            DesignLevelManager._register_system(subsystem, tmp_sys, tmp_ports, tmp_connections, hier_names_level)

    def _generate_system_contracts(self, system: System):
        system._convert_system_contract_to_contract_object()
        for subsystem in system.subsystems.values():
            self._generate_system_contracts(system=subsystem)

    def summary(self):
        print(f"======== Design Manager Summary ========")
        print(f"     Systems: {len(self._systems)}")
        print(f"     Ports: {len(self._ports)}")
        print(f"     Connections: {len(self._connections)}")

    def get_system(self, name: str) -> System | None:
        if name in self._systems:
            return self._systems[name]
        else:
            return None
        
    def get_port(self, name: str) -> Port | None:
        if name in self._ports:
            return self._ports[name]
        else:
            return None

    def get_connection(self, name: str) -> Connection | None:
        if name in self._connections:
            return self._connections[name]
        else:
            return None

    def get_design(self, name: str) -> System | None:
        if name in self._designs:
            return self._designs[name]
        else:
            return None
        
    def _verify_system_obj_or_str(self, system: str | System) :
        if isinstance(system, str):
            system_obj = self.get_system(system)
        elif isinstance(system, System):
            system_obj = system
        else:
            LOG.error(f"argument system must be a instance of string or System")
            raise Exception(f"Type Error")

        if system_obj is None:
            message = f"System \"{system}\" not exists"
            LOG.error(message)
            raise ObjectNotFoundException(message)
        if system_obj.hier_name not in self._systems:
            message = f"System object \"{system_obj.hier_name}\" not exists"
            LOG.error(message)
            raise ObjectNotFoundException(message)
        if self.get_system(system_obj.hier_name) != system_obj:
            message = f"System registered not matched with the instance"
            LOG.error(message)
            raise ObjectNotFoundException(message)
        return system_obj
    
    def _verify_design_obj_or_str(self, design: str | System) :
        if isinstance(design, str):
            design_obj = self.get_design(design)
        elif isinstance(design, System):
            design_obj = design
        else:
            LOG.error(f"argument design must be a instance of string or System")
            raise Exception(f"Type Error")

        if design_obj is None:
            message = f"Design \"{design}\" not exists"
            LOG.error(message)
            raise ObjectNotFoundException(message)
        if design_obj.hier_name not in self._systems:
            message = f"Design object \"{design_obj.hier_name}\" not exists"
            LOG.error(message)
            raise ObjectNotFoundException(message)
        if self.get_system(design_obj.hier_name) != design_obj:
            message = f"Design registered not matched with the instance"
            LOG.error(message)
            raise ObjectNotFoundException(message)
        return design_obj

def _build_hier_name(hier_names):
    return ".".join(hier_names)
    

def _decode_hier_name(hier_name):
    return hier_name.split(".")



