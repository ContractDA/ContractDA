import json
from contractda.design_api import DesignLevelManager
from contractda.simulator import ClauseEvaluator
from contractda.sets import FOLClauseSet

def test_design_simulation():
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    system = mgr.get_system("sim_sys_1.sub2")
    stimulus = {system.ports["a"]: 7}
    ret = mgr.simulate_system(system="sim_sys_1.sub2", stimulus=stimulus)
    assert(len(ret) == 1)
    assert(ret[0].value(var = system.ports["a"].var) == 7)
    assert(ret[0].value(var = system.ports["t2"].var) == 14)


def test_design_simulation_level():
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
        assert(value <= 2.4*7 and value >= 2.0*7)

# def test_design_evaluation():
#     design_path = "./example/design_files/simple_design_simulation.json"
#     mgr = DesignLevelManager()
#     mgr.read_design_from_file(file_path=design_path)

#     system = mgr.get_system("sim_sys_1")
#     stimulus = {system.ports["a"]: 7}
#     eval = ClauseEvaluator(FOLClauseSet(vars = [x, y, obj], expr= "obj == x+y"), clause_objective=[obj])
#     ret = mgr.simulate_system(system="sim_sys_1", stimulus=stimulus, system_compose_level=1, num_unique_simulations=5)
#     assert(len(ret) == 5)
#     for behavior in ret:
#         assert(behavior.value(var = system.ports["a"].var) == 7)
#         value = behavior.value(var = system.ports["x"].var)
#         assert(value <= 2.4*7 and value >= 2.0*7)

def test_design_autosimulation():
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)
    _,_,_ = mgr.auto_simulate_system(system="sim_sys_1")
