
from contractda.design._system import System, Port, Connection, SystemContract
from contractda.logger._logger import LOG
from contractda.design._design_exceptions import IncompleteContractException, ObjectNotFoundException
from contractda.simulator import Simulator, ClauseEvaluator, Evaluator, Stimulus
from contractda.design_api._design_expression import DesignExpression

from typing import Any
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
        """Verify if the given design satisfy refinement relation, hierarchical mean if the relation need to checked hierarchically
        
        A system is independent design safe if all the refinement of its subsystem contract satisfy strong replaceability
        
        """
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
        # check refinement
        if not self.verify_system_refinement(system=system):
            LOG.info("Not passing independent test because refinement not held")
            return False

        # check receptiveness
        receptive_flag = True
        irreceptive_contracts = self.verify_system_receptiveness(system=system)
        if irreceptive_contracts:
            receptive_flag = False
        for subsystem in system.subsystems.values():
            irreceptive_contracts = self.verify_system_receptiveness(system=subsystem)
            if irreceptive_contracts:
                receptive_flag = False    

        if system_obj.is_cascade():
            LOG.info("Cascade composition")
            if receptive_flag:
                LOG.info("All Subsystem are receptive, Independent Design OK")
                return True
            else:
                # remember to set input variables....
                LOG.info("Incllude non-receptive contract, checking strong replaceability")
                system_contract = system_obj._get_single_system_contract()
                subsystem_composed_contract = system_obj._get_subsystem_contract_composition()
                connection_constraint = system_obj._generate_contract_system_connection_constraint()
                input_vars = [port.var for port in system_obj.input_ports]
                LOG.info(f"Length of input vars: {len(input_vars)}")
                system_contract.add_constraint(connection_constraint, adjusted_input=input_vars)
                subsystem_composed_contract.add_constraint(connection_constraint, adjusted_input=input_vars)
                return system_contract.is_strongly_replaceable_by(subsystem_composed_contract)
        
        # feedback
        if len(system_obj.subsystems.values()) == 2:
            LOG.info("Feedback Composition, checking...")
            system_contract = system_obj._get_single_system_contract()
            subsystems = list(system_obj.subsystems.values())
            subsystem_contract1 = subsystems[0]._get_single_system_contract()
            subsystem_contract2 = subsystems[1]._get_single_system_contract()
            connection_constraint = system_obj._generate_contract_system_connection_constraint()
            input_vars = [port.var for port in system_obj.input_ports]
            LOG.info(f"Length of input vars: {len(input_vars)}")
            LOG.info(" ".join([var.id for var in input_vars]))
            print(subsystem_contract1)
            system_contract.add_constraint(connection_constraint, adjusted_input=input_vars)
            # get the input port vars, and make it consistent with system inputs.
            c1_input_vars = [port.var for port in subsystems[0].input_ports]
            c2_input_vars = [port.var for port in subsystems[1].input_ports]
            # create a map that maps subsystem ports to the corresponding system ports
            input_map = dict()
            for connection in system_obj.connections.values():
                sys_var = None
                for term in connection.terminals:
                    if term.var in input_vars:
                        sys_var = term.var 
                        break
                if sys_var is not None:
                    for term in connection.terminals:
                        input_map[term.var] = sys_var
            LOG.info(input_map)
            new_c1_input_vars = []
            for var in c1_input_vars:
                if var in input_map:
                    new_c1_input_vars.append(input_map[var])
                else:
                    new_c1_input_vars.append(var)

            new_c2_input_vars = []
            for var in c2_input_vars:
                if var in input_map:
                    new_c2_input_vars.append(input_map[var])
                else:
                    new_c2_input_vars.append(var)

            LOG.info(" ".join([port.var.id for port in subsystems[0].input_ports]))

            subsystem_contract1.add_constraint(connection_constraint, adjusted_input=new_c1_input_vars)
            LOG.info(" ".join([port.var.id for port in subsystems[1].input_ports]))
            subsystem_contract2.add_constraint(connection_constraint, adjusted_input=new_c2_input_vars)

            return system_contract.is_independent_decomposition_of(other1=subsystem_contract1, other2=subsystem_contract2)
        
        raise NotImplementedError("Not support when feedback composition has more than 2 subsystems")

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

    def verify_design_receptiveness(self, design: str | System, hierarchical=True) -> dict[System, list[SystemContract]]:
        """Check if the system contracts in a design are receptive

        :param str | System system: the system instance or its name for checking contract consistency
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        system_obj = self._verify_design_obj_or_str(design=design)
        systems_under_test = [system_obj]
        failed_contracts: dict[System, list[SystemContract]] = {}
        while systems_under_test:
            test_system = systems_under_test.pop()
            irreceptive_contracts = self.verify_system_receptiveness(test_system)
            if irreceptive_contracts:
                failed_contracts[test_system] = irreceptive_contracts
            
            systems_under_test.extend(list(test_system.subsystems.values()))
        return failed_contracts

    def verify_system_receptiveness(self, system: str | System, hierarchical=True) -> list[SystemContract]:
        """Check if the contracts in a system are receptive

        :param str | System system: the system instance or its name for checking contract consistency
        :param VarType | str port_type: the type of the port
        :param PortDirection | str direction: the direction of the port. See PortDirection
        """
        system_obj = self._verify_system_obj_or_str(system=system)
        self._generate_system_contracts(system_obj)
        irreceptive_contracts = []
        for contract in system_obj.contracts:
            if not contract.contract_obj.is_receptive():
                irreceptive_contracts.append(contract)
        return irreceptive_contracts

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

    def simulate_design(self, design: str | System, stimulus: Stimulus | dict[Port, Any], num_unique_simulations: int = 1) -> list[Stimulus]:
        """Simulate the design system using the stimulus

        :param: str | System design: the design for simulation
        :param Stimulus | dict[Port, Any] stimulus: the stimulus to set for the simulation
        :param int num_unique_simulations: number of unique behaviors want to perform for this simulation
        :return: the simulation result as stimulus
        :rtype: list[Stimulus]
        
        """
        system_obj = self._verify_design_obj_or_str(design=design)
        return self.simulate_system(system=system_obj, stimulus=stimulus, num_unique_simulations=num_unique_simulations)


    def evaluate_system(self, system: str | System, 
                        objective: DesignExpression,
                        stimulus: Stimulus | dict[Port, Any] = None, 
                        environement: DesignExpression = None,
                        system_compose_level:int|None = None) -> list[Any]:
        # TODO: allow control layer of composition
        system_obj = self._verify_system_obj_or_str(system=system)
        self._generate_system_contracts(system_obj)

        simulate_stimulus = None
        if isinstance(stimulus, Stimulus):
            simulate_stimulus = stimulus
        elif stimulus is not None:
            simulate_stimulus = Stimulus(port_stimulus_map=stimulus)

        # collect all vars     
        all_system_vars = [port.var for port in self._ports.values()]
        simulate_environment = None
        if environement is not None:
            simulate_environment = environement.get_clause_set(design_vars=all_system_vars)
        
        simulator = Simulator(system=system_obj, system_compose_level=system_compose_level)
        evaluator = ClauseEvaluator(clause_set=objective.get_clause_set(design_vars=all_system_vars),
                                    clause_objective=objective.aux_vars)
        ret = simulator.evaluate(stimulus=simulate_stimulus, 
                                 environement=simulate_environment, 
                                 evaluator=evaluator,
                                 check_unique=False)
        return ret

    def evaluate_range_system(self, system: str | System, 
                            objective: DesignExpression,
                            stimulus: Stimulus | dict[Port, Any] = None, 
                            environement: DesignExpression = None,
                            system_compose_level:int|None = None) -> list[Any]:
        # TODO: allow control layer of composition
        system_obj = self._verify_system_obj_or_str(system=system)
        self._generate_system_contracts(system_obj)

        simulate_stimulus = None
        if isinstance(stimulus, Stimulus):
            simulate_stimulus = stimulus
        elif stimulus is not None:
            simulate_stimulus = Stimulus(port_stimulus_map=stimulus)

        # collect all vars     
        all_system_vars = [port.var for port in self._ports.values()]
        simulate_environment = None
        if environement is not None:
            simulate_environment = environement.get_clause_set(design_vars=all_system_vars)
        
        simulator = Simulator(system=system_obj, system_compose_level=system_compose_level)
        evaluator = ClauseEvaluator(clause_set=objective.get_clause_set(design_vars=all_system_vars),
                                    clause_objective=objective.aux_vars)
        ret = simulator.evaluate_range(stimulus=simulate_stimulus, 
                                 environement=simulate_environment, 
                                 evaluator=evaluator)
        return ret

    
    def simulate_system(self, 
                        system: str | System, 
                        stimulus: Stimulus | dict[Port, Any], 
                        environement: DesignExpression = None,
                        num_unique_simulations: int = 1, 
                        system_compose_level:int|None = None) -> list[Stimulus]:
        """Simulate the system using the stimulus

        :param: str | System system: the system for simulation
        :param Stimulus | dict[Port, Any] stimulus: the stimulus to set for the simulation
        :param int num_unique_simulations: number of unique behaviors want to perform for this simulation
        :param int system_compose_level: number of level to perform composition, if not given, the whole system is used
        :return: the simulation result as stimulus
        :rtype: list[Stimulus]
        
        """

        system_obj = self._verify_system_obj_or_str(system=system)
        self._generate_system_contracts(system_obj)
        if isinstance(stimulus, Stimulus):
            simulate_stimulus = stimulus
        else:
            simulate_stimulus = Stimulus(port_stimulus_map=stimulus)

        all_system_vars = [port.var for port in self._ports.values()]
        simulate_environment = None
        if environement is not None:
            simulate_environment = environement.get_clause_set(design_vars=all_system_vars)
        
        simulator = Simulator(system=system_obj, 
                              system_compose_level=system_compose_level)
        ret = simulator.simulate(stimulus=simulate_stimulus, 
                                 environement=simulate_environment,
                                 num_unique_simulations=num_unique_simulations)
        return ret

    def auto_simulate_system(self, system: str | System, num_unique_simulations:int = 1, max_depth:int = 3)-> tuple[list[tuple[list[Stimulus], list[Stimulus]]], dict[Stimulus, list[tuple[list[Stimulus], list[Stimulus]]]]]:
        """Automatic simulate the system

        :param: str | System system: the system for simulation
        :param int max_depth: the depth used to automatic generate stimulus
        :param int num_unique_simulations: number of unique behaviors want to perform for this simulation
        :return: the simulation result as stimulus
        :rtype: list[Stimulus]
        
        """

        system_obj = self._verify_system_obj_or_str(system=system)
        self._generate_system_contracts(system_obj)
        simulator = Simulator(system=system_obj, system_compose_level=0)
        # should we allow auto simulation for system? set to 1 to avoid considering composition of subsystem
        environment_pairs, ret = simulator.auto_simulate(num_unique_simulations=num_unique_simulations, max_depth=max_depth)
        return environment_pairs, ret
    
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
            LOG.error(f"System {name} does not exist!")
            return None
        
    def get_port(self, name: str) -> Port | None:
        if name in self._ports:
            return self._ports[name]
        else:
            LOG.error(f"Port {name} does not exist!")
            return None

    def get_connection(self, name: str) -> Connection | None:
        if name in self._connections:
            return self._connections[name]
        else:
            LOG.error(f"Connection {name} does not exist!")
            return None

    def get_design(self, name: str) -> System | None:
        if name in self._designs:
            return self._designs[name]
        else:
            LOG.error(f"Design {name} does not exist!")
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



