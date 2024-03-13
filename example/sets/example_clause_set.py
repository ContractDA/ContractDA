from contractda.sets import ClauseSet, FOLClauseSet
from contractda.vars._var import IntVar, BoolVar, RealVar, CategoricalVar

if __name__ == "__main__":

    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    a = BoolVar("a")
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
    clause = FOLClauseSet(vars=[x, y, z],expr="(x + y + z) ^ 3 == 8 && x == 2 && y != 3")
    assert(clause.is_satifiable())
    # clause = FOLClauseSet(vars=[a, x, y, z],expr="(a == false) && (x + y + z) ^ 3 == 8 && x == 2 && y != 3")
    # assert(clause.is_satifiable())
    clause = FOLClauseSet(vars=[a, x, y, z],expr="(a == true) && (x + y + z) ^ 3 == 8 && x == 2 && y != 3")
    assert(clause.is_satifiable())
    clause = FOLClauseSet(vars=[a, x, y, z],expr="!a && (x + y + z) ^ 3 == 8 && x == 2 && y != 3")
    assert(clause.is_satifiable())