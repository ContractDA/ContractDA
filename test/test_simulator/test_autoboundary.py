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

def test_autosim_boundary_generate_eq(x, y):
    c = AGContract([x, y], assumption="x == 5", guarantee="y <= 2*x && y >= 1.8*x")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 1)
    for example_ins, example_outs in examples:
        assert(len(example_ins) == 1)
        assert(str(example_ins[0]) == "(x==5.0)")
        assert(len(example_outs) == 1)
        assert(str(example_outs[0]) == "(x!=5.0)")

def test_autosim_boundary_generate_neq(x, y):
    c = AGContract([x, y], assumption="x != 5", guarantee="y <= 2*x && y >= 1.8*x")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 1)
    for example_ins, example_outs in examples:
        assert(len(example_ins) == 1)
        assert(str(example_ins[0]) == "(x!=5.0)")
        assert(len(example_outs) == 1)
        assert(str(example_outs[0]) == "(x==5.0)")

def test_autosim_boundary_generate_lt(x, y):
    c = AGContract([x, y], assumption="x < 5", guarantee="y <= 2*x && y >= 1.8*x")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 1)
    for example_ins, example_outs in examples:
        assert(len(example_ins) == 1)
        assert(str(example_ins[0]) == "(x<5.0)")
        assert(len(example_outs) == 2)
        assert(str(example_outs[0]) == "(x==5.0)")
        assert(str(example_outs[1]) == "(x>5.0)")

def test_autosim_boundary_generate_le(x, y):
    c = AGContract([x, y], assumption="x <= 5", guarantee="y <= 2*x && y >= 1.8*x")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 1)
    for example_ins, example_outs in examples:
        assert(len(example_ins) == 2)
        assert(str(example_ins[0]) == "(x<5.0)")
        assert(str(example_ins[1]) == "(x==5.0)")
        assert(len(example_outs) == 1)
        assert(str(example_outs[0]) == "(x>5.0)")

def test_autosim_boundary_generate_ge(x, y):
    c = AGContract([x, y], assumption="x >= 5", guarantee="y <= 2*x && y >= 1.8*x")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 1)
    for example_ins, example_outs in examples:
        assert(len(example_ins) == 2)
        assert(str(example_ins[0]) == "(x==5.0)")
        assert(str(example_ins[1]) == "(x>5.0)")
        assert(len(example_outs) == 1)
        assert(str(example_outs[0]) == "(x<5.0)")

def test_autosim_boundary_generate_gt(x, y):
    c = AGContract([x, y], assumption="x > 5", guarantee="y <= 2*x && y >= 1.8*x")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 1)
    for example_ins, example_outs in examples:
        assert(len(example_ins) == 1)
        assert(str(example_ins[0]) == "(x>5.0)")
        assert(len(example_outs) == 2)
        assert(str(example_outs[0]) == "(x<5.0)")
        assert(str(example_outs[1]) == "(x==5.0)")

def test_autosim_boundary_generate_and(x, y, z):
    c = AGContract([x, y, z], assumption="x <= 5 && y >= 3", guarantee="z == x + y")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 3)

def test_autosim_boundary_generate_or(x, y, z):
    c = AGContract([x, y, z], assumption="x <= 5 || y >= 3", guarantee="z == x + y")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 3)

def test_autosim_boundary_generate_implies(x, y, z):
    c = AGContract([x, y, z], assumption="x <= 5 -> y >= 3", guarantee="z == x + y")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 3)

def test_autosim_boundary_generate_multi_neg(x, y, z):
    c = AGContract([x, y, z], assumption="(x <= 5 && x >= 3) || (!(y >= 3))", guarantee="z == x + y")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 6)

def test_autosim_boundary_generate_multi_and_or(x, y, z):
    c = AGContract([x, y, z], assumption="(x <= 5 && x >= 3) || (y >= 3 && y<= 4)", guarantee="z == x + y")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 7)


def test_autosim_boundary_generate_and_empty_clean(x, y, z):
    c = AGContract([x, y, z], assumption="x <= 5 && x >= 3", guarantee="z == x + y")

    examples = c.assumption.generate_boundary_set_linear()
    assert(len(examples) == 3)

