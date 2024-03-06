from contractda.sets.explicit_set import ExplicitSet

if __name__ == "__main__":
    values = [(1, 2, 3), (2, 3, 4), (1, 3, 5)]
    vars = ["x", "w", "z"]

    eset = ExplicitSet(vars, values)
    print(eset)

    for elem in eset:
        print(elem)

    print(eset.sample())
    print(eset.internal_vars)
    print(eset.internal_values)
    print(eset.ordered_vars)
    print(eset.ordered_values)
