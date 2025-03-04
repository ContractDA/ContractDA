from contractda.design_api import DesignLevelManager, DesignExpression
from contractda.simulator import Simulator, Stimulus, ClauseEvaluator
from contractda.vars import RealVar
from contractda.sets import FOLClauseSet

def test_evaluation():
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    obj = RealVar("obj")

    system = mgr.get_system("sim_sys_1")
    system.report()
    stimulus = {system.ports["a"]: 5}
    print(stimulus)
    ret = mgr.evaluate_system(system="sim_sys_1", 
                              objective=DesignExpression(expr="obj == sim_sys_1.a + sim_sys_1.x", aux_vars=[obj], clause_type=FOLClauseSet),
                              stimulus=stimulus,
                              system_compose_level=0)
    assert(len(ret) == 1)
    assert(ret[0] >= 5*3 and ret[0] <= 5*4)

def test_evaluation_level():
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    obj = RealVar("obj")

    system = mgr.get_system("sim_sys_1")
    system.report()
    stimulus = {system.ports["a"]: 5}
    print(stimulus)
    ret = mgr.evaluate_system(system="sim_sys_1", 
                              objective=DesignExpression(expr="obj == sim_sys_1.a + sim_sys_1.x", aux_vars=[obj], clause_type=FOLClauseSet),
                              stimulus=stimulus,
                              system_compose_level=1)
    assert(len(ret) == 1)
    assert(ret[0] >= 5*3 and ret[0] <= 5*3.4)

def test_evaluation_env():
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    obj = RealVar("obj")

    system = mgr.get_system("sim_sys_1")
    system.report()
    ret = mgr.evaluate_system(system="sim_sys_1", 
                              objective=DesignExpression(expr="obj == sim_sys_1.a + sim_sys_1.x", aux_vars=[obj], clause_type=FOLClauseSet),
                              environement=DesignExpression(expr="sim_sys_1.a >= 4 && sim_sys_1.a <= 4.5"),
                              system_compose_level=0)
    assert(len(ret) == 1)
    assert(ret[0] >= 4*3 and ret[0] <= 4.5*4)

def test_evaluation_env_level():
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    obj = RealVar("obj")

    system = mgr.get_system("sim_sys_1")
    system.report()
    ret = mgr.evaluate_system(system="sim_sys_1", 
                              objective=DesignExpression(expr="obj == sim_sys_1.a + sim_sys_1.x", aux_vars=[obj], clause_type=FOLClauseSet),
                              environement=DesignExpression(expr="sim_sys_1.a >= 4 && sim_sys_1.a <= 4.5"),
                              system_compose_level=1)
    assert(len(ret) == 1)
    assert(ret[0] >= 4*3 and ret[0] <= 4.5*3.4)

def test_evaluation_range():
    design_path = "./example/design_files/simple_design_simulation.json"
    mgr = DesignLevelManager()
    mgr.read_design_from_file(file_path=design_path)

    obj = RealVar("obj")

    system = mgr.get_system("sim_sys_1")
    system.report()
    ret = mgr.evaluate_range_system(system="sim_sys_1", 
                              objective=DesignExpression(expr="obj == sim_sys_1.a + sim_sys_1.x", aux_vars=[obj], clause_type=FOLClauseSet),
                              environement=DesignExpression(expr="sim_sys_1.a >= 3 && sim_sys_1.a <= 4"),
                              system_compose_level=0)
    assert(ret == ([16.0], [9.0]))