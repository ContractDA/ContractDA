from contractda.simulator import Simulator, Stimulus, ClauseEvaluator
from contractda.contracts import CBContract
from contractda.vars import Var, RealVar, IntVar
from contractda.sets import FOLClauseSet
import pytest

def test_simulator():
    I = RealVar("I")
    V = RealVar("V")
    c = CBContract([I, V], constraint="I*V <= 8", behavior="V == 2*I")

    sti = Stimulus({V: 4})
    sim = Simulator(contract=c)
    ret = sim.simulate(stimulus=sti)
    assert(len(ret) == 1)
    for behavior in ret:
        for var, val in behavior.var_val_map.items():
            if var.get_id() == "V":
                assert(val == 4)
            if var.get_id() == "I":
                assert(val == 2)

def test_simulator_env():
    I = RealVar("I")
    V = RealVar("V")
    c = CBContract([I, V], constraint="I*V <= 8", behavior="V == 2*I")

    env = FOLClauseSet(vars = [I, V], expr="V >= 1 && V <= 2")
    sim = Simulator(contract=c)
    ret = sim.simulate(environement=env, num_unique_simulations=20)
    assert(len(ret) == 20)
    for behavior in ret:
        V_val = behavior.var_val_map[V]
        I_val = behavior.var_val_map[I]
        assert(V_val >= 1 and V_val <= 2)
        assert(V_val == 2*I_val)
        print(V_val, I_val)

def test_simulator_multiple_behave():
    I = RealVar("I")
    V = RealVar("V")
    c = CBContract([I, V], constraint="I*V <= 10", behavior="V <= 2.1*I && V >= 1.9*I")

    sti = Stimulus({V: 4})
    sim = Simulator(contract=c)
    ret = sim.simulate(stimulus=sti, num_unique_simulations=5)
    assert(len(ret) == 5)
    for behavior in ret:
        for var, val in behavior.var_val_map.items():
            if var.get_id() == "V":
                assert(val == 4)
            if var.get_id() == "I":
                assert(val <= 4/1.9 and val >= 4/2.1)

def test_evaluator():
    I = RealVar("I")
    V = RealVar("V")
    c = CBContract([I, V], constraint="I*V <= 8", behavior="V == 2*I")

    sti = Stimulus({V: 4})

    sti = Stimulus({V: 4})
    obj = RealVar("obj")
    eval = ClauseEvaluator(FOLClauseSet(vars = [I, V, obj], expr= "obj == I*V"), clause_objective=[obj])
    
    sim = Simulator(contract=c, evaluator= eval)
    obj_val = sim.evaluate(stimulus=sti)
    assert(obj_val == [8])
    obj_val = sim.evaluate_range(stimulus=sti)
    assert(obj_val == ([8], [8]))

def test_evaluate_env():
    I = RealVar("I")
    V = RealVar("V")
    c = CBContract([I, V], constraint="I*V <= 8", behavior="V == 2*I")

    obj = RealVar("obj")
    env = FOLClauseSet(vars = [I, V], expr="V >= 1 && V <= 2")
    eval = ClauseEvaluator(FOLClauseSet(vars = [I, V, obj], expr= "obj == I+V"), clause_objective=[obj])
    sim = Simulator(contract=c, evaluator= eval)
    obj_val = sim.evaluate(environement=env)
    assert(obj_val[0] >= 1.5 and obj_val[0] <= 3)
    obj_val = sim.evaluate_range(environement=env)
    assert(obj_val == ([3.0], [1.5]))