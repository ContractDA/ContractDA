from contractda.sets import ClauseSet, FOLClauseSet
from contractda.vars._var import IntVar, BoolVar, RealVar, CategoricalVar
import itertools

def test_fol_clause_set_is_satisfiable():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    clause = FOLClauseSet(vars=[x, y, z],expr="x + y == 4 && 2*x + 5 == 4")
    assert(clause.is_satifiable())
    clause = FOLClauseSet(vars=[x, y, z],expr="x + y == 1 || x + y == 10")
    assert(clause.is_satifiable())
    clause = FOLClauseSet(vars=[x, y, z],expr="x + y == 1 && x + y == 10")
    assert(not clause.is_satifiable())
    clause = FOLClauseSet(vars=[x, y, z],expr="x + y == y && x ^ 4 == 10")
    assert(not clause.is_satifiable())
    clause = FOLClauseSet(vars=[x, y, z],expr="(x + y) ^ 2 == 4 && x == 2")
    assert(clause.is_satifiable())

def test_fol_clause_set_is_contain():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && x - y >= 0 && x >= 3)")
    assert(clause1.is_contain({x: 3, y: 2, z: 6}) == True)
    assert(clause1.is_contain({x: 9, y: 2, z: 6}) == False)
    print("J???")
    for x_val, y_val, z_val in itertools.product(list(range(-50, 50)), list(range(-10, 10)), list(range(-10, 10))):
        assert(clause1.is_contain({x: x_val, y: y_val, z: z_val}) == (x_val + y_val <= 5 and x_val - y_val >= 0 and x_val >= 3))

    clause1 = FOLClauseSet(vars=[x, y, z],expr="true")
    assert(clause1.is_contain({x: 3, y: 2, z: 6}) == True)
    clause1 = FOLClauseSet(vars=[x, y, z],expr="false")
    assert(clause1.is_contain({x: 9, y: 2, z: 6}) == False)

def test_fol_clause_set_is_subset():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5) || (y == 5 && x <= 0))")
    assert(clause1.is_subset(clause2) == True)
    assert(clause2.is_subset(clause1) == True)
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5))")
    assert(clause1.is_subset(clause2) == False)
    assert(clause2.is_subset(clause1) == True)
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 6))")
    assert(clause1.is_subset(clause2) == True)
    assert(clause2.is_subset(clause1) == False)

def test_fol_clause_set_is_equivalent():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5) || (y == 5 && x <= 0))")
    assert(clause1.is_equivalence(clause2) == True)
    assert(clause2.is_equivalence(clause1) == True)
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5))")# (x = 0, y = 5) not in this one
    assert(clause1.is_equivalence(clause2) == False)
    assert(clause2.is_equivalence(clause1) == False)

def test_fol_clause_set_is_proper_subset():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5) || (y == 5 && x <= 0))")
    assert(clause1.is_proper_subset(clause2) == False)
    assert(clause2.is_proper_subset(clause1) == False)
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5))")
    assert(clause1.is_proper_subset(clause2) == False)
    assert(clause2.is_proper_subset(clause1) == True)
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 6))")
    assert(clause1.is_proper_subset(clause2) == True)
    assert(clause2.is_proper_subset(clause1) == False)

def test_fol_clause_set_is_disjoint():
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="(x + y > 10)")
    assert(clause1.is_disjoint(clause2) == True)
    assert(clause2.is_disjoint(clause1) == True)
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y >= 6 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="(x <= 1)")
    assert(clause1.is_disjoint(clause2) == False)
    assert(clause2.is_disjoint(clause1) == False)
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y >= 6 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="(x < 1)")
    assert(clause1.is_disjoint(clause2) == True)
    assert(clause2.is_disjoint(clause1) == True)