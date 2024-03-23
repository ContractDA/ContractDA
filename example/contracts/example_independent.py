from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, CategoricalVar
from contractda.sets import ExplicitSet
if __name__ == "__main__":
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
    
    cs.is_independent_decomposition_of(c1, c2)


    w = RealVar("w")
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
                    assumption="x >= 2 && x <= 3",
                    guarantee="((y == x * (y - 1) - x || x - 2 == 0) && y >= 1) || ((y + x * y == 0|| y == x - y)&& y < 1)")
    
    cs.is_independent_decomposition_of(c1, c2)
    # should be false if x >= 2, true if only x == 2
    # testcase 
    c1 = AGContract(vars=[x, y, z], 
                    assumption="x == x && z == z", 
                    guarantee="y == z + 1 || y == x * z")
    c2 = AGContract(vars=[y, z], 
                    assumption="y == y", 
                    guarantee="z == y + 1")
    cs = AGContract(vars=[x, y], 
                    assumption="x != 1", 
                    guarantee="y == x / (1 - x)")
    
    cs.is_independent_decomposition_of(c1, c2) # should be False

    # # classic testcase 1 (all type 3 good groups)
    # c1 = AGContract([x, y, z], 
    #                 assumption="x == x && y == y",
    #                 guarantee="z <= x + y + 3 && z >= x + y + 2")
    # c2 = AGContract([y, z], 
    #                 assumption="z == z",
    #                 guarantee="(y == 3)")
    # cs = AGContract([x, z], 
    #                 assumption="x >= -3",
    #                 guarantee="(z >= x + 5 && z <= x + 6)")
    
    # cs.is_independent_decomposition_of(c1, c2)
    # # should be True

    # # classic testcase 2 (with only type 3 that connected to type 2)
    # c1 = AGContract([x, y, z], 
    #                 assumption="x == x && y == y",
    #                 guarantee="z <= x + y + 3 && z >= x + y + 2")
    # c2 = AGContract([y, z], 
    #                 assumption="z == z",
    #                 guarantee="(y >= 3 && y <= 4)")
    # cs = AGContract([x, z], 
    #                 assumption="x >= -3",
    #                 guarantee="(z >= x + 5 && z <= x + 7)")
    
    # cs.is_independent_decomposition_of(c1, c2)
    # # should be False

    # # classic testcase 3 (type 3 in a loop)
    # c1 = AGContract([x, y, z], 
    #                 assumption="x == x && y == y",
    #                 guarantee="z <= 4 && z >= 3")
    # c2 = AGContract([y, z], 
    #                 assumption="z == z",
    #                 guarantee="(y >= 3 && y <= 4)")
    # cs = AGContract([x, z], 
    #                 assumption="x == x",
    #                 guarantee="z <= 4 && z >= 3")
    
    # cs.is_independent_decomposition_of(c1, c2)

    # # should be False

    # # classic testcase 4 (infinite type 3 chain)
    # c1 = AGContract([x, y, z], 
    #                 assumption="x == x && y == y",
    #                 guarantee="z == y + 1 || z == y - 1")
    # c2 = AGContract([y, z], 
    #                 assumption="z == z",
    #                 guarantee="(y == z + 1 || y == z - 1)")
    # cs = AGContract([x, z], 
    #                 assumption="x == x",
    #                 guarantee="z == z")
    
    # cs.is_independent_decomposition_of(c1, c2)

    # # should be False