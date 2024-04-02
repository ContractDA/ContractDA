from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, CategoricalVar
from contractda.sets import ExplicitSet

def test_inde_explicit_case_1():
    w = CategoricalVar("w", range(0, 5))
    x = CategoricalVar("x", range(0, 7))
    y = CategoricalVar("y", range(0, 8))
    z = CategoricalVar("z", range(0, 3))

    c1 = AGContract([w, x, y], 
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                                                    (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6),
                                                    (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6)]),
                    guarantee=ExplicitSet([w, x, y], [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 2, 2), (0, 3, 3), (0, 4, 3), (0, 5, 5), (0, 5, 6), (0, 6, 5), (0, 6, 6),
                                                      (1, 0, 0), (1, 0, 1), (1, 1, 1), (1, 3, 3), (1, 4, 3), (1, 5, 5), (1, 5, 6), (1, 6, 5), (1, 6, 6),
                                                      (2, 0, 0), (2, 0, 1), (2, 1, 1), (2, 4, 3), (2, 5, 5), (2, 5, 6), (2, 6, 5), (2, 6, 6)]))
    
    c2 = AGContract([x, y], 
                    assumption=ExplicitSet([y], [tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4]), tuple([5]), tuple([6])]),
                    guarantee=ExplicitSet([x, y], [(0, 1), (1, 1), (2, 2), (3, 3), (4, 3), (5, 5), (5, 6), (6, 5), (6, 6)]))
    
    cs = AGContract([w, x, y], 
                    assumption=ExplicitSet([w], [tuple([0]), tuple([1]), tuple([2])]),
                    guarantee=ExplicitSet([x, y], [(0, 1), (1, 1), (2, 2), (3, 3), (4, 3)]))
    
    assert(not cs.is_independent_decomposition_of(c1, c2))

    w = CategoricalVar("w", range(0, 5))
    x = CategoricalVar("x", range(0, 7))
    y = CategoricalVar("y", range(0, 8))
    z = CategoricalVar("z", range(0, 3))

    c1 = AGContract([w, x, y], 
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
                                                    (1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6)]),
                    guarantee=ExplicitSet([w, x, y], [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 2, 2), (0, 3, 3), (0, 4, 3), (0, 5, 5), (0, 5, 6), (0, 6, 5), (0, 6, 6),
                                                      (1, 0, 0), (1, 0, 1), (1, 1, 1), (1, 3, 3), (1, 4, 3), (1, 5, 5), (1, 5, 6), (1, 6, 5), (1, 6, 6)]))
    
    c2 = AGContract([x, y], 
                    assumption=ExplicitSet([y], [tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4]), tuple([5]), tuple([6])]),
                    guarantee=ExplicitSet([x, y], [(0, 1), (1, 1), (2, 2), (3, 3), (4, 3), (5, 5), (5, 6), (6, 5), (6, 6)]))
    
    cs = AGContract([w, x, y], 
                    assumption=ExplicitSet([w], [tuple([0]), tuple([1])]),
                    guarantee=ExplicitSet([x, y], [(0, 1), (1, 1), (2, 2), (3, 3), (4, 3)]))
    
    assert(cs.is_independent_decomposition_of(c1, c2))

def test_inde_explicit_case_2():
    w = CategoricalVar("w", range(0, 5))
    x = CategoricalVar("x", range(0, 7))
    y = CategoricalVar("y", range(0, 8))
    z = CategoricalVar("z", range(0, 3))

    c1 = AGContract([w, x, y], 
                    assumption=ExplicitSet([w, x], [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6)]),
                    guarantee=ExplicitSet([w, x, y], [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 2, 1)]))
    
    c2 = AGContract([x, y], 
                    assumption=ExplicitSet([y], [tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4]), tuple([5]), tuple([6])]),
                    guarantee=ExplicitSet([x, y], [(0, 0), (0, 1), (1, 1), (2, 1)]))
    
    cs = AGContract([w, x, y], 
                    assumption=ExplicitSet([w], [tuple([0])]),
                    guarantee=ExplicitSet([x, y], [(0, 0), (0, 1), (1, 1), (2, 1)]))
    
    assert(cs.is_independent_decomposition_of(c1, c2))
    #assert(False)

def test_inde_explicit_hard_case_1():
    x = CategoricalVar("x", range(0, 2))
    y = CategoricalVar("y", range(0, 5))
    z = CategoricalVar("z", range(0, 5))

    c1 = AGContract([x, y, z], # z <= x + y + 1, z >= x + y + 0
                    assumption=ExplicitSet([x, y], [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), 
                                                    (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]),
                    guarantee=ExplicitSet([x, y, z], [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 2), (0, 2, 2), (0, 2, 3), (0, 3, 3), (0, 3, 4), (0, 4, 4),
                                                      (1, 0, 1), (1, 0, 2), (1, 1, 2), (1, 1, 3), (1, 2, 3), (1, 2, 4), (1, 3, 4)]))
    
    c2 = AGContract([y, x], 
                    assumption=ExplicitSet([z], [tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4])]),
                    guarantee=ExplicitSet([z, y], [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)])) # y = 2
    
    cs = AGContract([x, z], 
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
                    guarantee=ExplicitSet([x, z], [(0, 2), (0, 3),
                                                   (1, 3), (1, 4)]))
    
    assert(cs.is_independent_decomposition_of(c1, c2))
    # assert(False)


def test_inde_explicit_hard_case_2():
    x = CategoricalVar("x", range(0, 2))
    y = CategoricalVar("y", range(0, 5))
    z = CategoricalVar("z", range(0, 5))

    c1 = AGContract([x, y, z], # z <= x + y + 1, z >= x + y + 0
                    assumption=ExplicitSet([x, y], [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), 
                                                    (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]),
                    guarantee=ExplicitSet([x, y, z], [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 2), (0, 2, 2), (0, 2, 3), (0, 3, 3), (0, 3, 4), (0, 4, 4),
                                                      (1, 0, 1), (1, 0, 2), (1, 1, 2), (1, 1, 3), (1, 2, 3), (1, 2, 4), (1, 3, 4)]))
    
    c2 = AGContract([y, x], 
                    assumption=ExplicitSet([z], [tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4])]),
                    guarantee=ExplicitSet([z, y], [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
                                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1)])) # y = 2 or 1
    
    cs = AGContract([x, z], 
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
                    guarantee=ExplicitSet([x, z], [(0, 1), (0, 2), (0, 3), 
                                                   (1, 2), (1, 3), (1, 4)]))
    
    assert(not cs.is_independent_decomposition_of(c1, c2))

def test_inde_explicit_hard_case_3():
    x = CategoricalVar("x", range(0, 2))
    y = CategoricalVar("y", range(0, 5))
    z = CategoricalVar("z", range(0, 5))

    c1 = AGContract([x, y, z], # z == 3 or z == 4
                    assumption=ExplicitSet([x, y], [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), 
                                                    (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]),
                    guarantee=ExplicitSet([x, y, z], [(0, 0, 3), (0, 0, 4), (0, 1, 3), (0, 1, 4), (0, 2, 3), (0, 2, 4), (0, 3, 3), (0, 3, 4), (0, 4, 3), (0, 4, 4),
                                                      (1, 0, 3), (1, 0, 4), (1, 1, 3), (1, 1, 4), (1, 2, 3), (1, 2, 4), (1, 3, 3), (1, 3, 4), (1, 4, 3), (1, 4, 4)]))
    
    c2 = AGContract([y, x], 
                    assumption=ExplicitSet([z], [tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4])]),
                    guarantee=ExplicitSet([z, y], [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
                                                   (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)])) # y = 3 or 4
    
    cs = AGContract([x, z], 
                    assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
                    guarantee=ExplicitSet([x, z], [(0, 3), (0, 4),
                                                   (1, 3), (1, 4)]))
    
    assert(not cs.is_independent_decomposition_of(c1, c2))

def test_inde_explicit_hard_case_4():
    # This cannot be done in explicit set as it is bounded...
    # x = CategoricalVar("x", range(0, 2))
    # y = CategoricalVar("y", range(0, 5))
    # z = CategoricalVar("z", range(0, 5))

    # c1 = AGContract([x, y, z], # z == y+1 or z == y-1
    #                 assumption=ExplicitSet([x, y], [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), 
    #                                                 (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]),
    #                 guarantee=ExplicitSet([x, y, z], [(0, 0, 3), (0, 0, 4), (0, 1, 3), (0, 1, 4), (0, 2, 3), (0, 2, 4), (0, 3, 3), (0, 3, 4), (0, 4, 3), (0, 4, 4),
    #                                                   (1, 0, 3), (1, 0, 4), (1, 1, 3), (1, 1, 4), (1, 2, 3), (1, 2, 4), (1, 3, 3), (1, 3, 4), (1, 4, 3), (1, 4, 4)]))
    
    # c2 = AGContract([y, x], 
    #                 assumption=ExplicitSet([z], [tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4])]),
    #                 guarantee=ExplicitSet([z, y], [(0, 3), (1, 3), (2, 3), (3, 3), (4, 3),
    #                                                (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)])) # y = 3 or 4
    
    # cs = AGContract([x, z], 
    #                 assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
    #                 guarantee=ExplicitSet([x, z], [(0, 3), (0, 4),
    #                                                (1, 3), (1, 4)]))
    
    # assert(not cs.is_independent_decomposition_of(c1, c2))
    assert(True)