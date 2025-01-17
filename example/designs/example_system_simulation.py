from contractda.design_api import DesignLevelManager
from contractda.simulator import Simulator, Stimulus, Evaluator

if __name__ == "__main__":
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    system = mgr.get_system("sim_sys_1")
    system._convert_system_contract_to_contract_object()
    system.report()
    simulator = Simulator(system=system)
    stimulus = Stimulus(port_stimulus_map={system.ports["a"]: 5})
    ret = simulator.simulate(stimulus=stimulus)
    print(ret[0])

    system = mgr.get_system("sim_sys_1.sub1")
    system._convert_system_contract_to_contract_object()
    system.report()
    simulator = Simulator(system=system)
    stimulus = Stimulus(port_stimulus_map={system.ports["a"]: 7})
    ret = simulator.simulate(stimulus=stimulus)
    print(ret[0])

    sim_behavior, violate_behavior, result = simulator.auto_simulate(max_depth=3, num_unique_simulations=1)
    for sim_behavior, ret in result.items():
        print(sim_behavior)
        for e in ret:
            print(" ", e)

    system = mgr.get_system("sim_sys_1.sub2")
    stimulus = {system.ports["a"]: 7}
    print(stimulus)
    ret = mgr.simulate_system(system="sim_sys_1.sub2", stimulus=stimulus)
    print(ret[0])

    sim, vio, ret = mgr.auto_simulate_system(system="sim_sys_1")
    for s, r in ret.items():
        print(s)
        for rr in r:
            print("  ", rr)