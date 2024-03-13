from contractda.sets import ClauseSet, FOLClause
from contractda.vars._var import IntVar, BoolVar, RealVar, CategoricalVar

if __name__ == "__main__":

    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    clause = ClauseSet(vars=[x, y, z],expr="x + y == 4 && x * y == 4", clause_type=FOLClause)
    clause.check_satifiable()