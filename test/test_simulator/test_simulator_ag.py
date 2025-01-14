from contractda.simulator import Simulator, Stimulus, ClauseEvaluator
from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, IntVar
from contractda.sets import FOLClauseSet
import pytest

def test_simulator():
    x = RealVar("x")
    y = RealVar("y")
    c = AGContract([x, y], assumption="x >= 0", guarantee="y == 2*x")

    sti = Stimulus({x: 50})
    sim = Simulator(contract=c)
    ret = sim.simulate(stimulus=sti)
    assert(len(ret) == 1)
    for behavior in ret:
        for var, val in behavior.var_val_map.items():
            if var.get_id() == "x":
                assert(val == 50)
            if var.get_id() == "y":
                assert(val == 100)

def test_simulator_multiple_behave():
    x = RealVar("x")
    y = RealVar("y")
    c = AGContract([x, y], assumption="x >= 0", guarantee="y == 2*x || y == 2*x + 1")

    sti = Stimulus({x: 50})
    sim = Simulator(contract=c)
    ret = sim.simulate(stimulus=sti, num_unique_simulations=2)
    assert(len(ret) == 2)
    for behavior in ret:
        for var, val in behavior.var_val_map.items():
            if var.get_id() == "x":
                assert(val == 50)
            if var.get_id() == "y":
                assert(val == 100 or val == 101)

def test_evaluator():
    x = RealVar("x")
    y = RealVar("y")
    c = AGContract([x, y], assumption="x >= 0", guarantee="y == 2*x")

    sti = Stimulus({x: 50})
    obj = RealVar("obj")
    eval = ClauseEvaluator(FOLClauseSet(vars = [x, y, obj], expr= "obj == x+y"), clause_objective=[obj])
    
    sim = Simulator(contract=c, evaluator= eval)
    obj_val = sim.evaluate(stimulus=sti)
    assert(obj_val == [150])
    obj_val = sim.evaluate_range(stimulus=sti)
    assert(obj_val == ([150], [150]))