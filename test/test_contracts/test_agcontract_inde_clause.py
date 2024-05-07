from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, CategoricalVar
from contractda.sets import ExplicitSet, FOLClauseSet

def test_inde_clause_case_1():
    # contain a type 1 fixed points for x == 2
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract([x, y, z], 
                    assumption="x == x && z == z",
                    guarantee="y == x * z || y == x + z")
    c2 = AGContract([y, z], 
                    assumption="y == y",
                    guarantee="(z == y - 2 && y >= 1) || ((z == 0 - y) && y < 1)")
    cs = AGContract([x, y], 
                    #assumption="x >= 2 && x <= 3",
                    assumption="x == 2",
                    guarantee="((y == x * (y - 1) - x || x - 2 == 0) && y >= 1) || ((y + x * y == 0|| y == x - y)&& y < 1)")
    
    assert(cs.is_independent_decomposition_of(c1, c2))
    # should be True

# def test_inde_clause_case_1_2():
#     x = RealVar("x")
#     y = RealVar("y")
#     z = RealVar("z")

#     c1 = AGContract([x, y, z], 
#                     assumption="x == x && z == z",
#                     guarantee="y == x * z || y == x + z")
#     c2 = AGContract([y, z], 
#                     assumption="y == y",
#                     guarantee="(z == y - 2 && y >= 1) || ((z == 0 - y) && y < 1)")
#     cs = AGContract([x, y], 
#                     assumption="x >= 2 && x <= 3",
#                     guarantee="((y == x * (y - 1) - x || x - 2 == 0) && y >= 1) || ((y + x * y == 0|| y == x - y)&& y < 1)")

#     assert(not cs.is_independent_decomposition_of(c1, c2))

    # should be False


def test_inde_clause_case_2():
    # all type 2 fixed points
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract(vars=[x, y, z], 
                    assumption="x == x && z == z", 
                    guarantee="y == z + 1 || y == x * z")
    c2 = AGContract(vars=[y, z], 
                    assumption="y == y", 
                    guarantee="z == y + 1")
    cs = AGContract(vars=[x, y], 
                    assumption="x != 1", 
                    guarantee="y == x / (1 - x)")
    
    assert(not cs.is_independent_decomposition_of(c1, c2))
    # should be False

def test_inde_clause_hard_case_1():
    # hard testcase 1 (all type 3 good groups)
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract([x, y, z], 
                    assumption="x == x && y == y",
                    guarantee="z <= x + y + 3 && z >= x + y + 2")
    c2 = AGContract([y, z], 
                    assumption="z == z",
                    guarantee="(y == 3)")
    cs = AGContract([x, z], 
                    assumption="x >= -3",
                    guarantee="(z >= x + 5 && z <= x + 6)")
    
    assert(cs.is_independent_decomposition_of(c1, c2))
    # should be True

def test_inde_clause_hard_case_2():
    # hard testcase 2 (with only type 3 that connected to type 2)
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract([x, y, z], 
                    assumption="x == x && y == y",
                    guarantee="z <= x + y + 2.5 && z >= x + y + 2")
    c2 = AGContract([y, z], 
                    assumption="z == z",
                    guarantee="(y >= 3 && y <= 3.5)")
    cs = AGContract([x, z], 
                    assumption="x >= -3",
                    guarantee="(z >= x + 5 && z <= x + 6)")
    
    assert(not cs.is_independent_decomposition_of(c1, c2))
    # should be False

def test_inde_clause_hard_case_3():
    # hard testcase 3 (type 3 in a loop)
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract([x, y, z], 
                    assumption="x == x && y == y",
                    guarantee="z <= 4 && z >= 3")
    c2 = AGContract([y, z], 
                    assumption="z == z",
                    guarantee="(y >= 3 && y <= 4)")
    cs = AGContract([x, z], 
                    assumption="x == x",
                    guarantee="z <= 4 && z >= 3")
    
    assert(not cs.is_independent_decomposition_of(c1, c2))
    # should be False

def test_inde_clause_hard_case_4():
    # hard testcase 4 (infinite type 3 chain)
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")

    c1 = AGContract([x, y, z], 
                    assumption="x == x && y == y",
                    guarantee="z == y + 1 || z == y - 1")
    c2 = AGContract([y, z], 
                    assumption="z == z",
                    guarantee="(y == z + 1 || y == z - 1)")
    cs = AGContract([x, z], 
                    assumption="x == x",
                    guarantee="z == z")
    
    assert(not cs.is_independent_decomposition_of(c1, c2))

    # should be False



