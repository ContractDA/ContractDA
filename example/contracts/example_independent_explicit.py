from contractda.contracts import AGContract
from contractda.vars import Var, RealVar, CategoricalVar
from contractda.sets import ExplicitSet
if __name__ == "__main__":

    # hard_case_1 all good type 3
    # x = CategoricalVar("x", range(0, 2))
    # y = CategoricalVar("y", range(0, 5))
    # z = CategoricalVar("z", range(0, 5))

    # c1 = AGContract([x, y, z], # z <= x + y + 1, z >= x + y + 0
    #                 assumption=ExplicitSet([x, y], [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), 
    #                                                 (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]),
    #                 guarantee=ExplicitSet([x, y, z], [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 2), (0, 2, 2), (0, 2, 3), (0, 3, 3), (0, 3, 4), (0, 4, 4),
    #                                                   (1, 0, 1), (1, 0, 2), (1, 1, 2), (1, 1, 3), (1, 2, 3), (1, 2, 4), (1, 3, 4)]))
    
    # c2 = AGContract([y, x], 
    #                 assumption=ExplicitSet([z], [tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4])]),
    #                 guarantee=ExplicitSet([z, y], [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)])) # y = 2
    
    # cs = AGContract([x, z], 
    #                 assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
    #                 guarantee=ExplicitSet([x, z], [(0, 2), (0, 3),
    #                                                (1, 3), (1, 4)]))
    
    # print(cs.is_independent_decomposition_of(c1, c2))

    # hard_case_2 unstable
    # x = CategoricalVar("x", range(0, 2))
    # y = CategoricalVar("y", range(0, 5))
    # z = CategoricalVar("z", range(0, 5))

    # c1 = AGContract([x, y, z], # z <= x + y + 1, z >= x + y + 0
    #                 assumption=ExplicitSet([x, y], [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), 
    #                                                 (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]),
    #                 guarantee=ExplicitSet([x, y, z], [(0, 0, 0), (0, 0, 1), (0, 1, 1), (0, 1, 2), (0, 2, 2), (0, 2, 3), (0, 3, 3), (0, 3, 4), (0, 4, 4),
    #                                                   (1, 0, 1), (1, 0, 2), (1, 1, 2), (1, 1, 3), (1, 2, 3), (1, 2, 4), (1, 3, 4)]))
    
    # c2 = AGContract([y, x], 
    #                 assumption=ExplicitSet([z], [tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4])]),
    #                 guarantee=ExplicitSet([z, y], [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2),
    #                                                (0, 1), (1, 1), (2, 1), (3, 1), (4, 1)])) # y = 2 or 1
    
    # cs = AGContract([x, z], 
    #                 assumption=ExplicitSet([x], [tuple([0]), tuple([1])]),
    #                 guarantee=ExplicitSet([x, z], [(0, 1), (0, 2), (0, 3), 
    #                                                (1, 2), (1, 3), (1, 4)]))
    
    # print(cs.is_independent_decomposition_of(c1, c2))

    # hard_case_2 loop
    # x = CategoricalVar("x", range(0, 2))
    # y = CategoricalVar("y", range(0, 5))
    # z = CategoricalVar("z", range(0, 5))

    # c1 = AGContract([x, y, z], # z == 3 or z == 4
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
    
    # print(cs.is_independent_decomposition_of(c1, c2))

    #example 1 in paper
    x = CategoricalVar("x", range(2, 3))
    y = CategoricalVar("y", range(-2, 5))
    z = CategoricalVar("z", range(-1, 3))
    w = CategoricalVar("w", range(6))

    c1 = AGContract([x, y, z, w], # y = xz or y = x + z
                    assumption=ExplicitSet([x, z], [(2, -1), (2, 0), (2, 1), (2, 2)]),
                    guarantee=ExplicitSet([x, y, z, w], [(2, -2, -1, 4), (2, 0, 0, 4), (2, 2, 1, 4), (2, 4, 2, 4),
                                                         (2, 1, -1, 4), (2, 2, 0, 4), (2, 3, 1, 4), (2, 4, 2, 4)]))
    
    c2 = AGContract([y, z], 
                    assumption=ExplicitSet([y], [tuple([-2]), tuple([-1]), tuple([0]), tuple([1]), tuple([2]), tuple([3]), tuple([4])]),
                    guarantee=ExplicitSet([z, y], [(2, -2), (1, -1), (0, 0), (-1, 1), (0, 2), (1, 3), (2, 4)])) # y = 3 or 4
    
    cs = AGContract([x, z, w], # y = x |y - 1| - x or y = |y-1| - 1 + x
                    assumption=ExplicitSet([x], [tuple([2])]),
                    guarantee=ExplicitSet([x, z, w], [(2, 4, 4), (2, 0, 4), (2, -1, 4), (2, 1, 4), (2, 2, 4), (2, 3, 4)]))
    
    print(cs.is_independent_decomposition_of(c1, c2))