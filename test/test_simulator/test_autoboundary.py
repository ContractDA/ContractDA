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

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 2, node=c.assumption.expr.root)
    assert(len(ib) == 1)
    assert(str(ib[0]) == "(x==5.0)")
    assert(len(ob) == 1)
    assert(str(ob[0]) == "(x!=5.0)")

def test_autosim_boundary_generate_neq(x, y):
    c = AGContract([x, y], assumption="x != 5", guarantee="y <= 2*x && y >= 1.8*x")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 2, node=c.assumption.expr.root)
    assert(len(ib) == 1)
    assert(str(ib[0]) == "(x!=5.0)")
    assert(len(ob) == 1)
    assert(str(ob[0]) == "(x==5.0)")

def test_autosim_boundary_generate_lt(x, y):
    c = AGContract([x, y], assumption="x < 5", guarantee="y <= 2*x && y >= 1.8*x")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 2, node=c.assumption.expr.root)
    assert(len(ib) == 1)
    assert(str(ib[0]) == "(x<5.0)")
    assert(len(ob) == 2)
    assert(str(ob[0]) == "(x==5.0)")
    assert(str(ob[1]) == "(x>5.0)")

def test_autosim_boundary_generate_le(x, y):
    c = AGContract([x, y], assumption="x <= 5", guarantee="y <= 2*x && y >= 1.8*x")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 2, node=c.assumption.expr.root)
    assert(len(ib) == 2)
    assert(str(ib[0]) == "(x<5.0)")
    assert(str(ib[1]) == "(x==5.0)")
    assert(len(ob) == 1)
    assert(str(ob[0]) == "(x>5.0)")

def test_autosim_boundary_generate_ge(x, y):
    c = AGContract([x, y], assumption="x >= 5", guarantee="y <= 2*x && y >= 1.8*x")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 2, node=c.assumption.expr.root)
    assert(len(ib) == 2)
    assert(str(ib[0]) == "(x>5.0)")
    assert(str(ib[1]) == "(x==5.0)")
    assert(len(ob) == 1)
    assert(str(ob[0]) == "(x<5.0)")

def test_autosim_boundary_generate_gt(x, y):
    c = AGContract([x, y], assumption="x > 5", guarantee="y <= 2*x && y >= 1.8*x")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 2, node=c.assumption.expr.root)
    assert(len(ib) == 1)
    assert(str(ib[0]) == "(x>5.0)")
    assert(len(ob) == 2)
    assert(str(ob[0]) == "(x==5.0)")
    assert(str(ob[1]) == "(x<5.0)")

def test_autosim_boundary_generate_and(x, y, z):
    c = AGContract([x, y, z], assumption="x <= 5 && y >= 3", guarantee="z == x + y")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 2, node=c.assumption.expr.root)
    assert(len(ib) == 4)
    assert(len(ob) == 5)

def test_autosim_boundary_generate_or(x, y, z):
    c = AGContract([x, y, z], assumption="x <= 5 || y >= 3", guarantee="z == x + y")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 2, node=c.assumption.expr.root)
    assert(len(ib) == 8)
    assert(len(ob) == 1)

def test_autosim_boundary_generate_implies(x, y, z):
    c = AGContract([x, y, z], assumption="x <= 5 -> y >= 3", guarantee="z == x + y")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 2, node=c.assumption.expr.root)
    assert(len(ib) == 7)
    assert(len(ob) == 2)

def test_autosim_boundary_generate_multi_neg(x, y, z):
    c = AGContract([x, y, z], assumption="(x <= 5 && x >= 3) || (!(y >= 3))", guarantee="z == x + y")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 3, node=c.assumption.expr.root)
    assert(len(ib) == 17)
    assert(len(ob) == 10)

def test_autosim_boundary_generate_multi_and_or(x, y, z):
    c = AGContract([x, y, z], assumption="(x <= 5 && x >= 3) || (y >= 3 && y<= 4)", guarantee="z == x + y")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 3, node=c.assumption.expr.root)
    assert(len(ib) == 56)
    assert(len(ob) == 25)


def test_autosim_boundary_generate_and_empty_clean(x, y, z):
    c = AGContract([x, y, z], assumption="x <= 5 && x >= 3", guarantee="z == x + y")

    ib, ob = c.assumption._generate_boundary_set(d=1, max_depth = 2, node=c.assumption.expr.root, exclude_empty=True, vars = c.assumption.vars)
    assert(len(ib) == 3)
    assert(len(ob) == 2)

def test_autosim_public_boundary_generate_set(x, y, z):
    c = AGContract([x, y, z], assumption="x <= 5 && x >= 3", guarantee="z == x + y")

    ib, ob = c.assumption.generate_boundary_set(max_depth=3)
    assert(len(ib) == 3)
    assert(len(ob) == 2)

# def test_autosim_boundary_generate_le(x, y):
#     x = RealVar("x")
#     y = RealVar("y")
#     c = AGContract([x, y], assumption="x <= 5", guarantee="y <= 2*x && y >= 1.8*x")

#     ib, ob = c.assumption._boundary_create_branch(expr=c.assumption.expr)
#     assert(len(ib) == 2)
#     assert(str(ib[0]) == "(x<5.0)")
#     assert(str(ib[1]) == "(x==5.0)")
#     assert(len(ob) == 1)
#     assert(str(ob[0]) == "(x>5.0)")

# def test_autosim_boundary_generate_ge(x, y):
#     x = RealVar("x")
#     y = RealVar("y")
#     c = AGContract([x, y], assumption="x >= 5", guarantee="y <= 2*x && y >= 1.8*x")

#     ib, ob = c.assumption._boundary_create_branch(expr=c.assumption.expr)
#     assert(len(ib) == 2)
#     assert(str(ib[0]) == "(x>5.0)")
#     assert(str(ib[1]) == "(x==5.0)")
#     assert(len(ob) == 1)
#     assert(str(ob[0]) == "(x<5.0)")

# def test_autosim_boundary_generate_lt(x, y):
#     x = RealVar("x")
#     y = RealVar("y")
#     c = AGContract([x, y], assumption="x < 5", guarantee="y <= 2*x && y >= 1.8*x")

#     ib, ob = c.assumption._boundary_create_branch(expr=c.assumption.expr)
#     assert(len(ib) == 1)
#     assert(str(ib[0]) == "(x<5.0)")
#     assert(len(ob) == 2)
#     assert(str(ob[0]) == "(x==5.0)")
#     assert(str(ob[1]) == "(x>5.0)")

# def test_autosim_boundary_generate_gt(x, y):
#     x = RealVar("x")
#     y = RealVar("y")
#     c = AGContract([x, y], assumption="x > 5", guarantee="y <= 2*x && y >= 1.8*x")

#     ib, ob = c.assumption._boundary_create_branch(expr=c.assumption.expr)
#     assert(len(ib) == 1)
#     assert(str(ib[0]) == "(x>5.0)")
#     assert(len(ob) == 2)
#     assert(str(ob[0]) == "(x==5.0)")
#     assert(str(ob[1]) == "(x<5.0)")

# def test_autosim_boundary_generate_ineq(x, y):
#     x = RealVar("x")
#     y = RealVar("y")
#     c = AGContract([x, y], assumption="x != 5", guarantee="y <= 2*x && y >= 1.8*x")

#     ib, ob = c.assumption._boundary_create_branch(expr=c.assumption.expr)
#     assert(len(ib) == 1)
#     assert(str(ib[0]) == "(x!=5.0)")
#     assert(len(ob) == 1)
#     assert(str(ob[0]) == "(x==5.0)")

# def test_autosim_boundary_generate_and(x, y):
#     x = RealVar("x")
#     y = RealVar("y")
#     c = AGContract([x, y], assumption="x <= 5 && x >= 3", guarantee="y <= 2*x && y >= 1.8*x")

#     ib, ob = c.assumption._boundary_create_branch(expr=c.assumption.expr)
#     assert(len(ib) == 1)
#     assert(str(ib[0]) == "((x<=5.0)&&(x>=3.0))")
#     assert(len(ob) == 3)
#     assert(str(ob[0]) == "((x<=5.0)&&(!(x>=3.0)))")
#     assert(str(ob[1]) == "((!(x<=5.0))&&(x>=3.0))")
#     assert(str(ob[2]) == "((!(x<=5.0))&&(!(x>=3.0)))")

# def test_autosim_boundary_generate_and(x, y):
#     x = RealVar("x")
#     y = RealVar("y")
#     c = AGContract([x, y], assumption="x <= 5 || x >= 3", guarantee="y <= 2*x && y >= 1.8*x")

#     ib, ob = c.assumption._boundary_create_branch(expr=c.assumption.expr)
#     assert(len(ib) == 3)
#     assert(str(ib[0]) == "((x<=5.0)&&(x>=3.0))")
#     assert(str(ib[1]) == "((x<=5.0)&&(!(x>=3.0)))")
#     assert(str(ib[2]) == "((!(x<=5.0))&&(x>=3.0))")
#     assert(len(ob) == 1)
#     assert(str(ob[0]) == "((!(x<=5.0))&&(!(x>=3.0)))")

# def test_autosim_boundary_generate_imply(x, y):
#     x = RealVar("x")
#     y = RealVar("y")
#     c = AGContract([x, y], assumption="x <= 5 -> x >= 3", guarantee="y <= 2*x && y >= 1.8*x")

#     ib, ob = c.assumption._boundary_create_branch(expr=c.assumption.expr)
#     assert(len(ib) == 3)
#     assert(str(ib[0]) == "((x<=5.0)&&(x>=3.0))")
#     assert(str(ib[1]) == "((!(x<=5.0))&&(x>=3.0))")
#     assert(str(ib[2]) == "((!(x<=5.0))&&(!(x>=3.0)))")
#     assert(len(ob) == 1)
#     assert(str(ob[0]) == "((x<=5.0)&&(!(x>=3.0)))")
    