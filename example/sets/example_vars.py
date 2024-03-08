from contractda.sets.var import IntVar, BoolVar, RealVar, CategoricalVar

if __name__ == "__main__":
    int_a = IntVar("a")
    int_b = IntVar("b")
    bool_c = BoolVar("c")
    bool_d = BoolVar("d")
    real_e = RealVar("e")
    real_f = RealVar('f')
    range_g = CategoricalVar("g", range(1, 10, 2))
    range_h = CategoricalVar("h", range(10, 15, 1))

    print(int_a)
    print(int_b)
    print(range_g)
    print(range_h)
    print(real_e)
    print(real_f)


