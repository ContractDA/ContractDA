import pytest
from contractda.simulator import Simulator, Stimulus, ClauseEvaluator
from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, IntVar
from contractda.sets import FOLClauseSet

@pytest.fixture
def x():
    return RealVar("x")

@pytest.fixture
def y():
    return RealVar("y")

@pytest.fixture
def z():
    return RealVar("z")

def test_autosim(x, y, z):
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    c = AGContract([x, y, z], assumption="x <= 5 && y >= 3", guarantee="z == x + y || z == x*y")

    sim = Simulator(contract=c)

    environments, result = sim.auto_simulate(num_unique_simulations=2)
    for in_e, ex_e in environments:
        for e in in_e:
            print("success: ", e)
        for e in ex_e:
            print("fail: ", e)

    for sti, ret in result.items():
        print(sti)
        for associated_result in ret:
            print("    ", associated_result)
    