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
    sim_behavior, violate_behavior, result = mgr.auto_simulate_system(system="sim_sys_1.sub1", max_depth=3, num_unique_simulations=1)
    for sim_behavior, ret in result.items():
        print(sim_behavior)
        for e in ret:
            print(" ", e)

    print("4")
    system = mgr.get_system("sim_sys_1.sub2")
    stimulus = {system.ports["a"]: 7}
    print(stimulus)
    ret = mgr.simulate_system(system="sim_sys_1.sub2", stimulus=stimulus)
    print(ret[0])

    print("5")
    sim, vio, ret = mgr.auto_simulate_system(system="sim_sys_1")
    for s, r in ret.items():
        print(s)
        for rr in r:
            print("  ", rr)