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

    # projection
    a = RangeIntVar("a", range(1,3))
    b = RangeIntVar("b", range(1,3))
    c = RangeIntVar("c", range(1,3))
    d = RangeIntVar("d", range(1,5))
    e = RangeIntVar("e", range(1,4))
    vars = [b, a, c]
    values = [(1, 2, 1), (1, 2, 2), (1, 1, 1)]
    test_set = ExplicitSet(vars, values)
    test1 = test_set.project([b, a], is_refine=False)
    test2 = test_set.project([a, b], is_refine=True)
    test3 = test_set.project([a, b, d, e], is_refine=False)
    test4 = test_set.project([b, a, e, d], is_refine=True)

    print(test1._values_internal, [var.id for var in test1._vars])
    print(test1)
    print(test2)
    print(test3)
    print(test4)

    print("")
    print("Complement")
    test1 = test_set.complement()
    print(test1)

    str_a = RangeIntVar("str_a", ["abc", "test", "454"])
    str_b = RangeIntVar("str_b", ["abc", "444", "555"])
    values = [("abc", "444"), ("454", "444")]
    test_set = ExplicitSet([str_a, str_b], values=values)
    print(test_set)
    print(test_set.complement())
