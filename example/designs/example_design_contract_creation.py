import json
from contractda.design._system import System
from contractda.sets._fol_clause_set import FOLClauseSet
from contractda.design._design_mgr import DesignLevelManager

if __name__ == "__main__":
    with open("./example/design_files/simple_design.json", "r") as file:
        json_obj = json.load(file)

    sys = System.from_dict(json_obj)
    design_mgr = DesignLevelManager()
    design_mgr.register_design(sys)

    design = design_mgr.get_design("test_sys")
    design.report()
    print(design)

    sys1 = design_mgr.get_system("test_sys.sub1")
    sys1.report()
    for port_name, port in sys1.ports.items():
        print(port)
        port.report()

    design_mgr._generate_system_contracts(system=sys)
    for contract in sys.contracts:
        print(contract._contract_obj)

    design_mgr.verify_system_consistensy(system=sys)

    print(sys._check_terminal_directions(list(sys.connections.values())[0]))

    constraint = sys._generate_contract_system_connection_constraint()
    print(constraint)

    print(sys._get_single_system_contract())
    print(sys._get_subsystem_contract_composition())
    print(sys._get_contract_language_type())
    print(design_mgr.verify_system_refinement(system=sys))
    print(design_mgr.verify_design_consistensy(design=sys))
