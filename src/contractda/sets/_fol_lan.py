""" First order logic language definition

This source file defines the abstract syntax tree (AST) of First-order logic.
"""
from abc import ABC, abstractmethod


class AST_Node(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def get_symbols(self):
        return {}
    
    @abstractmethod
    def evaluate(self, value_table = dict):
        pass

def name_remap(name_map, node):
    for name, s in node.get_symbols().items():
        s.name = name_map[name]

class PropositionNode(AST_Node):
    # Proposition: Proposition ==&&||-> Proposition
    #              Expression <=>===<> Expression
    #              !Proposition
    #              (Proposition)

    def __init__(self):
        pass


class PropositionNodeBinOp(PropositionNode):
    def __init__(self, op, exp1, exp2):
        self.exp1 = exp1
        self.exp2 = exp2
        self.op = op

    def __str__(self):
        return str(self.exp1) + str(self.op) + str(self.exp2)

    def get_symbols(self):
        l_symbols = self.exp1.get_symbols()
        r_symbols = self.exp2.get_symbols()
        res = l_symbols.copy()
        res.update(r_symbols)
        return res

    def debug(self):
        print("Exp 1:" )

    def evaluate(self, value_table = dict) -> bool:
        if self.op == "==":
            return self.exp1.evaluate(value_table) == self.exp2.evaluate(value_table)
        elif self.op == "<=":
            return self.exp1.evaluate(value_table) <= self.exp2.evaluate(value_table)
        elif self.op == "<":
            return self.exp1.evaluate(value_table) < self.exp2.evaluate(value_table)
        elif self.op == ">":
            return self.exp1.evaluate(value_table) > self.exp2.evaluate(value_table)
        elif self.op == ">=":
            return self.exp1.evaluate(value_table) >= self.exp2.evaluate(value_table)
        elif self.op == "!=":
            return self.exp1.evaluate(value_table) != self.exp2.evaluate(value_table)
        elif self.op == "&&":
            return self.exp1.evaluate(value_table) and self.exp2.evaluate(value_table)
        elif self.op == "||":
            return self.exp1.evaluate(value_table) or self.exp2.evaluate(value_table)
        elif self.op == "->":
            return (not self.exp1.evaluate(value_table)) or self.exp2.evaluate(value_table)
        else:
            raise Exception(f"Unsupported operator: {self.op}")

class PropositionNodeUniOp(PropositionNode):#(!Proposition)
    def __init__(self, op, exp1):
        self.exp1 = exp1
        self.op = op

    def __str__(self):
        return str(self.op) + str(self.exp1)

    def get_symbols(self):
        return self.exp1.get_symbols()
    
    def evaluate(self, value_table: dict):
        if self.op == "!":
            return not self.exp1.evaluate(value_table)
        else:
            raise Exception(f"Unsupported operator: {self.op}")
           
class PropositionNodeParen(PropositionNode):#(!Proposition)
    def __init__(self, content):
        self.content = content

    def __str__(self):
        return "(" + str(self.content) + ")"

    def get_symbols(self):
        return self.content.get_symbols()  

    def evaluate(self, value_table: dict):
        return self.content.evaluate(value_table)
# class UnaryOp(AST_Node):
#     def __init__(self, left, op, right):
#         self.left = left
#         self.op = op
#         self.right = right
#     def __str__(self):
#         return str(self.left) + self.op + str(self.right)
class ExpressionNode(AST_Node):
    # Literals/Constant +-*/^ Literals/Constant
    # Literals/Constant +-*/^ Expressions
    # Expression +-*/^ Expressions
    # (Expression)
    # Literals
    def __init__(self, content):
        pass

class ExpressionNodeParen(ExpressionNode): # (Expression)
    # Literals

    def __init__(self, content):
        self.content = content

    def __str__(self):
        return "(" + str(self.content) + ")"

    def get_symbols(self):
        return self.content.get_symbols()   

    def evaluate(self, value_table: dict):
        return self.content.evaluate(value_table)

class ExpressionNodeBinOp(ExpressionNode):
                                             # Expression +-*/^ Literals/Constant
                                             # Expression +-*/^ Expressions
    def __init__(self, op, left, right):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return str(self.left) + str(self.op) + str(self.right)

    def get_symbols(self):
        l_symbols = self.left.get_symbols()
        r_symbols = self.right.get_symbols()
        res = l_symbols.copy()
        res.update(r_symbols)
        return res
    
    def evaluate(self, value_table: dict):
        if self.op == "+":
            return self.left.evaluate(value_table) + self.right.evaluate(value_table)
        elif self.op == "-":
            return self.left.evaluate(value_table) - self.right.evaluate(value_table)
        elif self.op == "*":
            return self.left.evaluate(value_table) * self.right.evaluate(value_table)
        elif self.op == "/":
            return self.left.evaluate(value_table) / self.right.evaluate(value_table)
        elif self.op == "^":
            return self.left.evaluate(value_table) ** self.right.evaluate(value_table)
        else:
            raise Exception(f"Unsupported operator: {self.op}")

class TFNode(AST_Node):
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return self.val
    def get_symbols(self):
        return {} 
    
    def evaluate(self, value_table: dict):
        if self.val == "true":
            return True
        elif self.val == "false":
            return False
        else:
            raise Exception(f"Unsupported TF value: {self.val}")

class Symbol(AST_Node): # Literals
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def get_symbols(self):
        return {self.name: self}
    def evaluate(self, value_table: dict):
        value = value_table.get(self.name)
        if value is None:
            raise Exception(f"No symbol value found for: {self.name}")
        return value

class Constant(AST_Node): # Constant
    def __init__(self, val):
        self.val = val
    def __str__(self):
        return str(self.val)
    def get_symbols(self):
        return {}
    def evaluate(self, value_table: dict):
        return self.val