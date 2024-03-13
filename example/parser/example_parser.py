
from contractda.sets.parsers._fol_parser import FOL_Lexer, fol_parser
import contractda.sets._fol_lan as _fol_lan

import copy

if __name__ == "__main__":
    lexer = FOL_Lexer()
    lexer.build()
    lexer.test("5 > x && (c_54 < x) -> (50 + 54 * 44e-5 == -5) % || (true == false + 5 + fuck^3) # test an")
    print("")
    lexer.test("abc == TRDEGF")
    print("")
    lexer.test("x + y <= 100")
    print("")
    lexer.test("x + y <= 100.44")
    print("")
    lexer.test("x & y == false")
    print(lexer.tokens)


    ast = fol_parser.test("5 > x && !((c_54 < x) -> (50 + 54 * 44e-5 == -5)) # 1jijij jfaiji")
    print(ast)
    print(isinstance(ast, _fol_lan.PropositionNode))
    print(ast.get_symbols())
    symbols = ast.get_symbols()
    name_map = {"x": "y", "c_54": "c_64"}
    _fol_lan.name_remap(name_map, ast)
    print(ast)
    print("")
    # parser = FOL_Parser()
    # parser.build()
    fol_parser.reset()
    print(fol_parser._ctx)
    ast = fol_parser.test("(x + y <= 100)")
    print(ast)
    print(ast.get_symbols())
    print(ast.evaluate({"x": 29, "y": 100}))
    print("")
    ast = fol_parser.parse("(z == x + y -> x^5 >= 3) && true")
    print(ast)
    print(ast.get_symbols())
    ast_copy = copy.deepcopy(ast)
    print(ast_copy)
    print(ast_copy.get_symbols())
    print(ast.evaluate({"x": 29, "y": 100, "z": 129}))
    print(ast.evaluate({"x": 1, "y": 100, "z": 101}))
    print(ast.evaluate({"x": False, "y": 100, "z": 101}))

    ast = fol_parser.parse("true")
    print(ast)
    print(ast.get_symbols())
    print(ast.evaluate({"x": False, "y": 100, "z": 101}))



