from contractda.design_api import DesignLevelManager
from contractda.simulator import Simulator, Stimulus, Evaluator

if __name__ == "__main__":
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    print("1")
    system = mgr.get_system("sim_sys_1")
    system.report()
    stimulus = {system.ports["a"]: 5}
    print(stimulus)
    ret = mgr.simulate_system(system="sim_sys_1", stimulus=stimulus)
    print(ret[0])

    print("2")
    system = mgr.get_system("sim_sys_1.sub1")
    system.report()
    stimulus = {system.ports["a"]: 7}
    print(stimulus)
    ret = mgr.simulate_system(system="sim_sys_1.sub1", stimulus=stimulus)
    print(ret[0])

    print("3")
    environment_paris, result = mgr.auto_simulate_system(system="sim_sys_1.sub1", max_depth=3, num_unique_simulations=1)
    for sim_behavior, ret in result.items():
        print(sim_behavior)
        for ins, exs in ret:
            for i in ins:
                print(" ", i)
            for e in exs:
                print(" ", e)

    print("4")
    system = mgr.get_system("sim_sys_1.sub2")
    stimulus = {system.ports["a"]: 7}
    print(stimulus)
    ret = mgr.simulate_system(system="sim_sys_1.sub2", stimulus=stimulus)
    print(ret[0])

    print("5")
    environment_paris, ret = mgr.auto_simulate_system(system="sim_sys_1")
    for sim_behavior, ret in result.items():
        print(sim_behavior)
        for ins, exs in ret:
            for i in ins:
                print(" ", i)
            for e in exs:
                print(" ", e)

    print("6")
    system = mgr.get_system("sim_sys_1")
    contract = system._get_composed_system_contract(max_level=5)
    print(contract)

    contract = system._get_subsystem_contract_composition()
    print(contract)
    print(system.report())

    contract = system._get_composed_system_contract(max_level=0)
    print(contract)
    print("7")
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    system = mgr.get_system("sim_sys_1")
    stimulus = {system.ports["a"]: 7}
    ret = mgr.simulate_system(system="sim_sys_1", stimulus=stimulus, system_compose_level=1, num_unique_simulations=5)
    assert(len(ret) == 5)
    for behavior in ret:
        assert(behavior.value(var = system.ports["a"].var) == 7)
        value = behavior.value(var = system.ports["x"].var)
        print(value)
