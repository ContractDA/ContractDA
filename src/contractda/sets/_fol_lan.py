""" First order logic language definition

This source file defines the abstract syntax tree (AST) of First-order logic.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Callable, Any
import copy

class AST_Node(ABC):
    def __init__(self, children = None):
        if children is None:
            self._children = []
        else: 
            self._children = children
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

    @property
    def children(self):
        return self._children
    
    def recursive_process_preorder(self, process_func: Callable[..., Any], *args, **kwargs):
        process_func(self, *args, **kwargs)
        for child in self.children:
            child.recursive_process_preorder(process_func, *args, **kwargs)

    def recursive_process_postorder(self, process_func: Callable[..., Any], *args, **kwargs):
        for child in self.children:
            child.recursive_process_postorder(process_func, *args, **kwargs)
        process_func(self, *args, **kwargs)



def name_remap(name_map, node):
    def rename_recur_func(node: AST_Node, map: dict[str, str]):
        if isinstance(node, Symbol):
            name = node.name
            node.name = name_map[name]

    node.recursive_process_preorder(rename_recur_func, name_map)

class PropositionNode(AST_Node):
    # Proposition: Proposition ==&&||-> Proposition
    #              Expression <=>===<> Expression
    #              !Proposition
    #              (Proposition)

    def __init__(self, children = None):
        super().__init__(children=children)


class PropositionNodeBinOp(PropositionNode):
    def __init__(self, op, exp1, exp2):
        self.op = op
        super().__init__(children=[exp1, exp2])

    def __str__(self):
        return f"({self._children[0]}{self.op}{self._children[1]})"

    def get_symbols(self):
        l_symbols = self._children[0].get_symbols()
        r_symbols = self._children[1].get_symbols()
        res = l_symbols.copy()
        res.update(r_symbols)
        return res

    def debug(self):
        print("Exp 1:" )

    def evaluate(self, value_table = dict) -> bool:
        if self.op == "==":
            return self._children[0].evaluate(value_table) == self._children[1].evaluate(value_table)
        elif self.op == "<=":
            return self._children[0].evaluate(value_table) <= self._children[1].evaluate(value_table)
        elif self.op == "<":
            return self._children[0].evaluate(value_table) < self._children[1].evaluate(value_table)
        elif self.op == ">":
            return self._children[0].evaluate(value_table) > self._children[1].evaluate(value_table)
        elif self.op == ">=":
            return self._children[0].evaluate(value_table) >= self._children[1].evaluate(value_table)
        elif self.op == "!=":
            return self._children[0].evaluate(value_table) != self._children[1].evaluate(value_table)
        elif self.op == "&&":
            return self._children[0].evaluate(value_table) and self._children[1].evaluate(value_table)
        elif self.op == "||":
            return self._children[0].evaluate(value_table) or self._children[1].evaluate(value_table)
        elif self.op == "->":
            return (not self._children[0].evaluate(value_table)) or self._children[1].evaluate(value_table)
        else:
            raise Exception(f"Unsupported operator: {self.op}")

class PropositionNodeUniOp(PropositionNode):#(!Proposition)
    def __init__(self, op, exp1):
        self.exp1 = exp1
        self.op = op
        super().__init__(children=[exp1])

    def __str__(self):
        return f"({self.op}{self._children[0]})"

    def get_symbols(self):
        return self._children[0].get_symbols()
    
    def evaluate(self, value_table: dict):
        if self.op == "!":
            return not self._children[0].evaluate(value_table)
        else:
            raise Exception(f"Unsupported operator: {self.op}")
           
class PropositionNodeParen(PropositionNode):#(!Proposition)
    def __init__(self, content):
        super().__init__(children=[content])

    def __str__(self):
        return f"({self._children[0]})"

    def get_symbols(self):
        return self._children[0].get_symbols()  

    def evaluate(self, value_table: dict):
        return self._children[0].evaluate(value_table)
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
    def __init__(self, children = None):
        super().__init__(children=children)

class ExpressionNodeParen(ExpressionNode): # (Expression)
    # Literals

    def __init__(self, content):
        super().__init__(children=[content])

    def __str__(self):
        return f"({self._children[0]})"

    def get_symbols(self):
        return self._children[0].get_symbols()   

    def evaluate(self, value_table: dict):
        return self._children[0].evaluate(value_table)

class ExpressionNodeBinOp(ExpressionNode):
                                             # Expression +-*/^ Literals/Constant
                                             # Expression +-*/^ Expressions
    def __init__(self, op, left, right):
        self.op = op
        super().__init__(children=[left, right])

    def __str__(self):
        return f"{self._children[0]}{str(self.op)}{self._children[1]}"

    def get_symbols(self):
        l_symbols = self._children[0].get_symbols()
        r_symbols = self._children[1].get_symbols()
        res = l_symbols.copy()
        res.update(r_symbols)
        return res
    
    def evaluate(self, value_table: dict):
        if self.op == "+":
            return self._children[0].evaluate(value_table) + self._children[1].evaluate(value_table)
        elif self.op == "-":
            return self._children[0].evaluate(value_table) - self._children[1].evaluate(value_table)
        elif self.op == "*":
            return self._children[0].evaluate(value_table) * self._children[1].evaluate(value_table)
        elif self.op == "/":
            return self._children[0].evaluate(value_table) / self._children[1].evaluate(value_table)
        elif self.op == "^":
            return self._children[0].evaluate(value_table) ** self._children[1].evaluate(value_table)
        else:
            raise Exception(f"Unsupported operator: {self.op}")

class TFNode(AST_Node):
    def __init__(self, val):
        self.val = val
        super().__init__(children=None)
    def __str__(self):
        return self.val
    def get_symbols(self):
        return set() 
    
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
        super().__init__(children=None)

    def __str__(self):
        return self.name
    def get_symbols(self):
        return set([self.name])
    def evaluate(self, value_table: dict):
        value = value_table.get(self.name)
        if value is None:
            raise Exception(f"No symbol value found for: {self.name}")
        return value

class Constant(AST_Node): # Constant
    def __init__(self, val):
        self.val = val
        super().__init__(children=None)

    def __str__(self):
        return str(self.val)
    def get_symbols(self):
        return set()
    def evaluate(self, value_table: dict):
        return self.val