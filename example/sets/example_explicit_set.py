from contractda.sets.explicit_set import ExplicitSet
from contractda.sets.var import IntVar, BoolVar, RealVar, RangeIntVar

if __name__ == "__main__":
    v = RangeIntVar("v", range(1,10))
    w = RangeIntVar("w", range(1,10))
    x = RangeIntVar("x", range(1,10))
    y = RangeIntVar("y", range(1,10))
    z = RangeIntVar("z", range(1,10))
    

    a_values = [(1, 2, 3), (2, 3, 4), (1, 3, 5), (3, 3, 2), (1, 10, 23)]
    a_vars = [x, w, v]

    b_values = [(1, 2, 1), (2, 3, 4), (1, 3, 2)]
    b_vars = [y, z, x]

    c_values = [(1, 2, 3), (2, 3, 4), (1, 10, 23)]
    c_vars = [x, w, v]

    a_set = ExplicitSet(a_vars, a_values)
    b_set = ExplicitSet(b_vars, b_values)
    c_set = ExplicitSet(c_vars, c_values)
    print(a_set)
    print(b_set)
    print(c_set)

    for elem in a_set:
        print(elem)

    print(a_set.sample())
    print(a_set.internal_vars)
    print(a_set.internal_values)
    print(a_set.ordered_vars)
    print(a_set.ordered_values)

    oa_set = ExplicitSet.intersect(a_set, b_set)
    print(oa_set)

    ob_set = ExplicitSet.intersect(a_set, a_set)
    print(ob_set)

    oc_set = ExplicitSet.intersect(a_set, c_set)
    print(oc_set)


