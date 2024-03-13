from contractda.solvers.clause_set_solver import ClauseSetSolver
from contractda.solvers.z3_interface import Z3Interface
from contractda.sets._clause import FOLClause, Clause
from contractda.vars._var import Var, RealVar, IntVar, BoolVar, CategoricalVar

import contractda.sets._fol_lan as fol_lan

class FOLClauseSetSolver(ClauseSetSolver):
    """Class for solving FOL Clause
    """
    sort_map = ()
    def __init__(self, theory_prover = "z3"):
        if theory_prover == "z3":
            self._prover = Z3Interface
        else:
            raise Exception(f"Unsupported theory prover type {theory_prover}")
        pass

    def encode(self, vars: list[Var], clause: FOLClause):
        """Encode a first order logic clause into Z3 clauses"""
        # generate symbols in z3
        vars_map = {var.id: self._prover.get_fresh_variable(var.id, sort=var.type_str) for var in vars}
        # 
        root = clause.root
        z3clause = self._encode(vars_map=vars_map, node=root)
        return z3clause

    def _encode(self, vars_map, node: fol_lan.AST_Node):

        # recursively encode the ast
        if isinstance(node, fol_lan.PropositionNodeBinOp):
            z3_clause1 = self._encode(vars_map=vars_map, node=node.children[0])
            z3_clause2 = self._encode(vars_map=vars_map, node=node.children[1])
            if node.op == "==":
                return self._prover.clause_equal(z3_clause1, z3_clause2)
            elif node.op == "<=":
                return self._prover.clause_le(z3_clause1, z3_clause2)
            elif node.op == "<":
                return self._prover.clause_lt(z3_clause1, z3_clause2)
            elif node.op == ">":
                return self._prover.clause_gt(z3_clause1, z3_clause2)
            elif node.op == ">=":
                return self._prover.clause_ge(z3_clause1, z3_clause2)
            elif node.op == "!=":
                return self._prover.clause_neq(z3_clause1, z3_clause2)
            elif node.op == "&&":
                return self._prover.clause_and(z3_clause1, z3_clause2)
            elif node.op == "||":
                return self._prover.clause_or(z3_clause1, z3_clause2)
            elif node.op == "->":
                return self._prover.clause_implies(z3_clause1, z3_clause2)
            else:
                raise Exception(f"Unsupported operator: {node.op}")

        elif isinstance(node, fol_lan.PropositionNodeUniOp):
            z3_clause = self._encode(vars_map=vars_map, node=node.children[0])
            if node.op == "!":
                return self._prover.clause_not(z3_clause)
            else:
                raise Exception(f"Unsupported operator: {node.op}")

        elif isinstance(node, fol_lan.PropositionNodeParen):
            return self._encode(vars_map=vars_map, node=node.children[0])
        elif isinstance(node, fol_lan.ExpressionNodeParen):
            return self._encode(vars_map=vars_map, node=node.children[0])
        elif isinstance(node, fol_lan.ExpressionNodeBinOp):
            z3_clause1 = self._encode(vars_map=vars_map, node=node.children[0])
            z3_clause2 = self._encode(vars_map=vars_map, node=node.children[1])
            if node.op == "+":
                return z3_clause1 + z3_clause2
            elif node.op == "-":
                return z3_clause1 - z3_clause2
            elif node.op == "*":
                return z3_clause1 * z3_clause2
            elif node.op == "/":
                return z3_clause1 / z3_clause2
            elif node.op == "^":
                return z3_clause1 ** z3_clause2
            else:
                raise Exception(f"Unsupported operator: {node.op}")
            
        elif isinstance(node, fol_lan.TFNode):
            if node.val == "true":
                return True
            elif node.val == "false":
                return False
            else:
                raise Exception(f"Unsupported TF value: {node.val}")
            
        elif isinstance(node, fol_lan.Constant):
            return node.val

        elif isinstance(node, fol_lan.Symbol):
            id = node.name

            # this should be handled by clause set, to be removed
            z3var = vars_map.get(id, None)
            if z3var is None:
                raise Exception(f"Not specified varibles {id}") 
            
            return z3var
        
    
    def check_satifiable(self, vars: list[Var], set_expr: FOLClause) -> bool:
        encoded_clause = self.encode(vars=vars, clause=set_expr)
        prover_instance = self._prover()
        prover_instance.add_conjunction_clause(encoded_clause)
        ret = prover_instance.check()
        print(f"Sat? {ret}")
        print(prover_instance._model)
        return ret