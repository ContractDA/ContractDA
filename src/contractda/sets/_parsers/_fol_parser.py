
import ply.lex as lex
import ply.yacc as yacc
import re

import contractda.sets._fol_lan as _fol_lan
 

class FOL_Lexer(object):
    """First Order Logic Lexer
    
    """
    fol_tokens_symbol = {"CONSTANT": r"[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?",
                "LITERAL": r"[a-zA-Z_][a-zA-Z0-9_]*",
                # Logical symbol
                "AND": r"&&",
                "OR": r"||",
                "LT": r"<",
                "LE": r"<=",
                "GE": r">=",
                "GT": r">",
                "EQ": r"==",
                "NEQ": r"!=",
                "NOT": r"!",
                "IMPLY": r"->",
                "LAND": r"&",
                "LOR": r"|",
                # Temporal Logic Symbol
                # Arithmetic symbol
                "ADD": r"+",
                "SUB": r"-",
                "MUL": r"*",
                "DIV": r"/",
                "POWER": r"^",
                # Structural Symbol
                "LPAREN": r"(",
                "RPAREN": r")",
                "COMMENT": r"\#.*",}
    
    # reserved_keyword: handle the special keywords that would be identified as literals
    reserved_keyword =  {"TRUE": r"true",
                "FALSE": r"false",
                "FORALL": r"forall",
                "EXIST": r"exist",}
    
    def __init__(self):
        token_symbol = self.fol_tokens_symbol
        self.tokens = list(self.fol_tokens_symbol.keys()) + list(self.reserved_keyword.keys())
        self.reserved_type_map = {value: key for (key, value) in self.reserved_keyword.items()}

        self.t_AND = re.escape(token_symbol["AND"])
        self.t_OR = re.escape(token_symbol["OR"])
        self.t_LT = re.escape(token_symbol["LT"])
        self.t_LE = re.escape(token_symbol["LE"])
        self.t_GE = re.escape(token_symbol["GE"])
        self.t_GT = re.escape(token_symbol["GT"])
        self.t_EQ = re.escape(token_symbol["EQ"])
        self.t_NOT = re.escape(token_symbol["NOT"])
        self.t_NEQ = re.escape(token_symbol["NEQ"])
        self.t_IMPLY = re.escape(token_symbol["IMPLY"])
        self.t_LAND = re.escape(token_symbol["LAND"])
        self.t_LOR = re.escape(token_symbol["LOR"])
        # 
        self.t_ADD = re.escape(token_symbol["ADD"])
        self.t_SUB = re.escape(token_symbol["SUB"])
        self.t_MUL = re.escape(token_symbol["MUL"])
        self.t_DIV = re.escape(token_symbol["DIV"])
        self.t_POWER = re.escape(token_symbol["POWER"])
        #
        self.t_LPAREN = re.escape(token_symbol["LPAREN"])
        self.t_RPAREN = re.escape(token_symbol["RPAREN"])
        # 
        self.t_ignore = " \t"

    @lex.TOKEN(fol_tokens_symbol["CONSTANT"])
    def t_CONSTANT(self, t):
        t.value = float(t.value)
        return t

    @lex.TOKEN(fol_tokens_symbol["LITERAL"])
    def t_LITERAL(self, t):
        t.type = self.reserved_type_map.get(t.value, "LITERAL")
        return t

    @lex.TOKEN(fol_tokens_symbol["COMMENT"])
    def t_COMMENT(self, t):
        pass

    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok: 
                break
            print(tok)        

class FOL_Parser(object):
    """First Order Logic Parser
    
    """
    def __init__(self):
        
        lexer = FOL_Lexer()
        lexer.build()
        self.precedence = (("left", "LPAREN", "RPAREN"),
                           ("left", "AND", "OR", "IMPLY", "NOT"),
                           ("left", "GE", "GT", "LT", "LE", "EQ", "NEQ"),
                           ('left', 'ADD', 'SUB'),
                           ('left', 'MUL', 'DIV'),
                           ("left", "POWER"))
        self.tokens = lexer.tokens
        self._ctx = {}

    def p_proposition_uniop(self, p):
        '''proposition : NOT proposition
                       | NOT expression'''
        p[0] = _fol_lan.PropositionNodeUniOp(p[1], p[2])

    def p_proposition_binop(self, p):
        '''proposition : expression GE expression
                   | expression GT expression
                   | expression LT expression
                   | expression LE expression        
                   | expression EQ expression
                   | expression NEQ expression    
                   | proposition AND proposition   
                   | proposition OR proposition   
                   | proposition IMPLY proposition
                   | expression EQ proposition
                   | expression NEQ proposition
                   | proposition EQ expression
                   | proposition NEQ expression  '''
        p[0] = _fol_lan.PropositionNodeBinOp(p[2],p[1],p[3]) 
    def p_proposition_paren(self, p):   
        '''proposition : LPAREN proposition RPAREN'''
        p[0] = _fol_lan.PropositionNodeParen(p[2])

    def p_proposition_literal(self, p):   
        '''proposition : TRUE
                       | FALSE   '''
        p[0] = _fol_lan.TFNode(p[1])

    def p_expression_binop(self, p):
        '''expression : expression ADD expression
                   | expression SUB expression
                   | expression MUL expression
                   | expression DIV expression
                   | expression POWER expression'''

        p[0] = _fol_lan.ExpressionNodeBinOp(p[2],p[1],p[3])

    def p_expression_literal(self, p):
        '''expression : constant
                      | symbol'''
        p[0] = p[1]

    def p_expression_paren(self, p):
        '''expression : LPAREN expression RPAREN'''
        p[0] = _fol_lan.ExpressionNodeParen(p[2])

    def p_symbol(self, p):
        '''symbol : LITERAL'''
        p[0] = _fol_lan.Symbol(p[1])
        # if p[1] not in self._ctx:
            
        #     self._ctx[p[1]] = p[0]
        # else:
        #     p[0] = self._ctx[p[1]]
        

    def p_constant(self, p):
        '''constant : CONSTANT'''
        p[0] = _fol_lan.Constant(p[1])

    # Error rule for syntax errors
    def p_error(self, p):
     print(f"Syntax error in input! {p}")
     raise Exception("Syntax Error")
 
 # Build the parser
    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def reset(self) -> None:
        self._ctx = {}

    def test(self, data):
        return self.parser.parse(data)
    
    def parse(self, data, ctx = None):
        if ctx is None:
            self._ctx = {}
        else:
            self._ctx = ctx

        res = self.parser.parse(data)
        self.reset()
        return res

# global parser
fol_parser = FOL_Parser()
fol_parser.build()
 
if __name__ == "__main__":
    parser = FOL_Parser()
    parser.build()
    ast = parser.test("5 > x && !((c_54 < x) -> (50 + 54 * 44e-5 == -5)) # 1jijij jfaiji")
    print(ast)
    print(isinstance(ast, _fol_lan.PropositionNode))
    print(ast.get_symbols())
    symbols = ast.get_symbols()
    name_map = {"x": "y", "c_54": "c_64"}
    _fol_lan.name_remap(name_map, ast)
    print(ast)
