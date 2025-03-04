import json
from contractda.design._system import System
from contractda.design_api import DesignLevelManager

def test_design_mgr():
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

def test_system_composition():
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    example_system = mgr.get_system("sim_sys_1")
    
    example_system._convert_system_contract_to_contract_object()
    for sub in example_system.subsystems.values():
        sub._convert_system_contract_to_contract_object()
    contract1 = example_system._get_composed_system_contract(max_level=0)
    contract2 = example_system._get_single_system_contract()
    assert(contract1[0] == contract2)
    example_system._get_composed_system_contract()