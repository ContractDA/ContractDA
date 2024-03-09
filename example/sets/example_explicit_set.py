from contractda.sets.explicit_set import ExplicitSet
from contractda.sets.var import IntVar, BoolVar, RealVar, CategoricalVar

if __name__ == "__main__":
    v = CategoricalVar("v", range(1,10))
    w = CategoricalVar("w", range(1,10))
    x = CategoricalVar("x", range(1,10))
    y = CategoricalVar("y", range(1,10))
    z = CategoricalVar("z", range(1,10))
    

    a_expr = [(1, 2, 3), (2, 3, 4), (1, 3, 5), (3, 3, 2), (1, 10, 23)]
    a_vars = [x, w, v]

    b_expr = [(1, 2, 1), (2, 3, 4), (1, 3, 2)]
    b_vars = [y, z, x]

    c_expr = [(1, 2, 3), (2, 3, 4), (1, 10, 23)]
    c_vars = [x, w, v]

    a_set = ExplicitSet(a_vars, a_expr)
    b_set = ExplicitSet(b_vars, b_expr)
    c_set = ExplicitSet(c_vars, c_expr)
    print(a_set)
    print(b_set)
    print(c_set)

    for elem in a_set:
        print(elem)

    print(a_set.sample())
    print(a_set.internal_vars)
    print(a_set.internal_expr)
    print(a_set.ordered_vars)
    print(a_set.ordered_expr)

    oa_set = ExplicitSet.intersect(a_set, b_set)
    print(oa_set)

    ob_set = ExplicitSet.intersect(a_set, a_set)
    print(ob_set)

    oc_set = ExplicitSet.intersect(a_set, c_set)
    print(oc_set)

    # projection
    print("")
    print("Projection")
    a = CategoricalVar("a", range(1,3))
    b = CategoricalVar("b", range(1,3))
    c = CategoricalVar("c", range(1,3))
    d = CategoricalVar("d", range(1,5))
    e = CategoricalVar("e", range(1,4))
    vars = [b, a, c]
    expr = [(1, 2, 1), (1, 2, 2), (1, 1, 1)]
    test_set = ExplicitSet(vars, expr)
    test1 = test_set.project([b, a], is_refine=False)
    test2 = test_set.project([a, b], is_refine=True)
    test3 = test_set.project([a, b, d, e], is_refine=False)
    test4 = test_set.project([b, a, e, d], is_refine=True)

    print(test1._expr_internal, [var.id for var in test1._vars])
    print(test1)
    print(test2)
    print(test3)
    print(test4)

    print("")
    print("Complement")
    test1 = test_set.complement()
    print(test1)

    print("")
    str_a = CategoricalVar("str_a", ["abc", "test", "454"])
    str_b = CategoricalVar("str_b", ["abc", "444", "555"])
    expr = [("abc", "444"), ("454", "444")]
    test_set = ExplicitSet([str_a, str_b], expr=expr)
    print(test_set)
    print(test_set.complement())

    print("")
    print("Example for difference")
    x = CategoricalVar("x", range(1,5))
    y = CategoricalVar("y", range(1,5))
    z = CategoricalVar("z", range(1,4))

    a_expr = [(1, 2), (2, 1), (3, 3), (3, 4)]
    b_expr = [(2, 2), (1, 2), (3, 4)]
    c_expr = [(2, 3), (1, 2)]

    a_set = ExplicitSet([y, x], a_expr)
    b_set = ExplicitSet([x, y], b_expr)
    c_set = ExplicitSet([y, z], c_expr)
    ret_set = a_set.difference(b_set)
    print("difference of a_set - b_set: ", ret_set)
    ret_set = a_set.difference(c_set)
    print("difference of a_set - c_set: ", ret_set)

    # union
    print("")
    print("Union")
    ret_set = a_set.union(b_set)
    print("union of a_set and b_set: ", ret_set)
    ret_set = a_set.union(c_set)
    print("union of a_set and c_set: ", ret_set)