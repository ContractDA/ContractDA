from contractda.sets import ClauseSet, FOLClauseSet
from contractda.vars._var import IntVar, BoolVar, RealVar, CategoricalVar
import itertools
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

    clause1 = FOLClauseSet(vars=[x, y],expr="x + y == 4 && 2*x + 5 == 4")
    clause2 = FOLClauseSet(vars=[a, y, z],expr="(a == true) && (y + z) ^ 3 == 8 && y != 3")
    ret = clause1.union(clause2)
    print(ret.expr.root, ret._vars)
    print(ret.is_satifiable())
    print("")
    ret = clause1.intersect(clause2)
    print(ret.expr.root, ret._vars)
    print(ret.is_satifiable())
    print("")
    ret = clause1.difference(clause2)
    print(ret.expr.root, ret._vars)
    print(ret.is_satifiable())

    print("")
    ret = clause1.complement()
    print(ret.expr.root, ret._vars)
    print(ret.is_satifiable())

    # projection
    clause1 = FOLClauseSet(vars=[x, y],expr="(y <= 10) -> (x + y <= 5)")
    print(clause1.expr.root, clause1._vars)
    clause2 = clause1.project([x, z], is_refine=True)
    print(clause2.expr.root, clause2._vars)
    #clause3 = clause1.project([x, z], is_refine=False) #this get exception due to parser error 
    # True
    #print(clause3.expr.root, clause3._vars)

    clause1 = FOLClauseSet(vars=[x, y],expr="(y <= 10 && y >= 5) -> (x + y <= 5)")
    print(clause1.expr.root, clause1._vars)
    clause2 = clause1.project([x, z], is_refine=True)
    print(clause2.expr.root, clause2._vars)
    clause1 = FOLClauseSet(vars=[x, y],expr="(y <= 10 && y >= 5) && (x + y <= 5)")
    clause3 = clause1.project([x, z], is_refine=False)
    #Or(x <= 0, Not(0 <= x))
    print(clause3.expr.root, clause3._vars)

    # is_contain
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && x - y >= 0 && x >= 3)")
    print(clause1.is_contain({x: 3, y: 2, z: 6}))
    print(clause1.is_contain({x: 9, y: 2, z: 6}))
    # is_contain
    clause1 = FOLClauseSet(vars=[x, y, z],expr="true")
    print(clause1.is_contain({x: 3, y: 2, z: 6}))
    clause1 = FOLClauseSet(vars=[x, y, z],expr="false")
    print(clause1.is_contain({x: 9, y: 2, z: 6}))

    # is_equivalent
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5) || (y == 5 && x <= 0))")
    print(clause1.is_equivalence(clause2))
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5))")
    print(clause1.is_equivalence(clause2))

    print("is_subset")
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5) || (y == 5 && x <= 0))")
    print(clause1.is_subset(clause2))
    print(clause2.is_subset(clause1))
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5))")
    print(clause1.is_subset(clause2))
    print(clause2.is_subset(clause1))
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 6))")
    print(clause1.is_subset(clause2))
    print(clause2.is_subset(clause1))

    print("is_proper_subset")
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5) || (y == 5 && x <= 0))")
    print(clause1.is_proper_subset(clause2))
    print(clause2.is_proper_subset(clause1))
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 5))")
    print(clause1.is_proper_subset(clause2))
    print(clause2.is_proper_subset(clause1))
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="((x + y <= 5 && y < 6))")
    print(clause1.is_proper_subset(clause2))
    print(clause2.is_proper_subset(clause1))


    print("is_disjoint")
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="(x + y > 10)")
    print(clause1.is_disjoint(clause2))
    print(clause2.is_disjoint(clause1))
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y >= 6 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="(x <= 1)")
    print(clause1.is_disjoint(clause2))
    print(clause2.is_disjoint(clause1))
    clause1 = FOLClauseSet(vars=[x, y],expr="(x + y >= 6 && y <= 5)")
    clause2 = FOLClauseSet(vars=[x, y],expr="(x < 1)")
    print(clause1.is_disjoint(clause2))
    print(clause2.is_disjoint(clause1))