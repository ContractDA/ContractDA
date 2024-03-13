from contractda.sets import ClauseSet, FOLClauseSet
from contractda.vars._var import IntVar, BoolVar, RealVar, CategoricalVar


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
