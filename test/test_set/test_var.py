from contractda.sets._var import CategoricalVar, BoolVar, IntVar, RealVar

def test_range():
    x = CategoricalVar("x", value_range=range(1, 10))
    assert(x.id == "x")
    assert(x.value_range == range(1, 10))
    assert(x.is_finite() == True)

def test_int():
    x = IntVar("x")
    assert(x.id == "x")
    assert(x.is_finite() == False)