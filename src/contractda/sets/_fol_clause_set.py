""" Class for ClauseSet
"""
from __future__ import annotations
from typing import Iterable, Callable, Any
import copy

from contractda.sets._clause_set import ClauseSet, ClauseSetVarType
from contractda.vars._var import Var
from contractda.sets._clause import Clause
import contractda.sets._fol_lan as fol_lan
from contractda.sets._fol_clause import FOLClause
from contractda.solvers import Z3Interface

from contractda.logger._logger import LOG



class FOLClauseSet(ClauseSet):
    """ClauseSet

    A Clause set is a set that use clause to describe the condition of the set
    
    Threrefore the clause set should be able to generate the context 
    When context is needed, go through the list of symbols and then store the Var in the astnode
    When two clause are combined, rename by changing the astnode in the tree or reply on context when created
    """
    def __init__(self, vars: ClauseSetVarType, expr: str, ctx = None):
        """ clause_type: the """
        # create the context
        self._expr: Clause = FOLClause(description = expr, ctx = ctx)
        # check if the variables are indeed mentioned in expr
        context_ok, failed_list = self._check_context(vars = vars, expr=self._expr)
        if not context_ok:
            failed_id = [var.get_id() for var in failed_list]
            raise Exception(f"Variables {failed_id} not specified in the description: {expr}")
        # store the 
        self._vars = vars
        # solver
        self._solver_type = Z3Interface
        pass

    ######################
    #   Extraction
    ######################
    def __iter__(self):
        pass
    
    def __next__(self):
        pass

    def get_enumeration(self) -> Iterable:
        """ Enumerate the set elements

        :return: An iterable object that can produce all elements
        :rtype: Iterable
        """
        pass

    def sample(self) -> Any:
        """ Sample an element in the set

        :return: any element that is in the set
        :rtype: Any
        """
        pass
    ######################
    #   Set Operation
    ######################
    def union(self, other: FOLClauseSet) -> FOLClauseSet:
        """ Union opration on set

        :param FOLClauseSet other: the set to be union with this set
        :return: A new set which represents the union of the two set
        :rtype: FOLClauseSet
        """
        new_expr_a = copy.deepcopy(self.expr)
        new_expr_b = copy.deepcopy(other.expr)
        try:
            new_vars = self._combine_vars(self._vars, other._vars)
        except:
            LOG.error("The two set is defined under different variables with the same identifier!")
        # TODO: catch the exception 
        new_expr_a.clause_or(new_expr_b)
        new_instance = __class__.__new__(__class__)
        new_instance._expr = new_expr_a
        new_instance._vars = new_vars
        new_instance._solver_type = self._solver_type
        return new_instance

    def intersect(self, other: FOLClauseSet) -> FOLClauseSet:
        """ Intersect opration on set

        :param FOLClauseSet other: the set to be intersect with this set
        :return: A new set which represents the intersect of the two set
        :rtype: FOLClauseSet
        """
        new_expr_a = copy.deepcopy(self.expr)
        new_expr_b = copy.deepcopy(other.expr)
        try:
            new_vars = self._combine_vars(self._vars, other._vars)
        except:
            LOG.error("The two set is defined under different variables with the same identifier!")
        # TODO: catch the exception 
        new_expr_a.clause_and(new_expr_b)
        new_instance = __class__.__new__(__class__)
        new_instance._expr = new_expr_a
        new_instance._vars = new_vars
        new_instance._solver_type = self._solver_type
        return new_instance

    def difference(self, other: FOLClauseSet) -> FOLClauseSet:
        """ Difference opration on set 

        :param FOLClauseSet other: the set to be difference with this set
        :return: A new set which represents the difference of the two set
        :rtype: FOLClauseSet
        """
        new_expr_a = copy.deepcopy(self.expr)
        new_expr_b = copy.deepcopy(other.expr)
        try:
            new_vars = self._combine_vars(self._vars, other._vars)
        except:
            LOG.error("The two set is defined under different variables with the same identifier!")
        # TODO: catch the exception 
        new_expr_b.clause_not()
        new_expr_a.clause_and(new_expr_b)
        new_instance = __class__.__new__(__class__)
        new_instance._expr = new_expr_a
        new_instance._vars = new_vars
        new_instance._solver_type = self._solver_type
        return new_instance

    def complement(self) -> FOLClauseSet:
        """ Complement opration on set 

        :return: A new set which represents the Complement of the set
        :rtype: FOLClauseSet
        """
        new_expr = copy.deepcopy(self.expr)
        new_expr.clause_not()
        new_instance = __class__.__new__(__class__)
        new_instance._expr = new_expr
        new_instance._vars = self._vars
        new_instance._solver_type = self._solver_type
        return new_instance

    def project(self, vars, is_refine = True):
        """ Projection opration on set 

        :param vars: the list of variables to be the projection result.
        :param bool is_refine: whether the projection is to result in refinement or abstraction
        :return: A new set which represents the Projection of the set on the input variables
        :rtype: FOLClauseSet
        """
        pass

    def is_contain(self, element: Any) -> bool:
        """ Check if the set is contain the element

        :param element: the element to be checked if it is contained in the set
        :return: True if the element is in the set. False if not.
        :rtype: bool
        """
        pass

    def is_subset(self, other: FOLClauseSet) -> bool:
        """ Check if the set is a subset of the other set

        :param FOLClauseSet other: the other set to be check if this set is a subset of it.
        :return: True if this set is a subset of the other set. False if not.
        :rtype: bool
        """
        pass

    def is_proper_subset(self, other: FOLClauseSet) -> bool:
        """ Check if the set is a proper subset of the other set

        :param FOLClauseSet other: the other set to be check if this set is a proper subset of it.
        :return: True if this set is a proper subset of the other set. False if not.
        :rtype: bool
        """
        pass

    def is_satifiable(self) -> bool:
        """ Check if the set is satisfiable, i.e., not empty

        :return: True if this set is satisfiable. False if not.
        :rtype: bool
        """
        solver_instance = self._solver_type()
        encoded_clause = self.encode(solver=solver_instance, vars=self._vars, clause=self._expr)
        solver_instance.add_conjunction_clause(encoded_clause)
        ret = solver_instance.check()
        LOG.debug(f"solving with internal clauses: {solver_instance.assertions()}")
        LOG.debug(f"Sat? {ret}")
        LOG.debug(f"model: {solver_instance._model}")
        return ret   
        pass

    def is_equivalence(self, other: FOLClauseSet) -> bool:
        """ Check if the set is equivalent to the other set

        :param FOLClauseSet other: the other set to be check if this set is equivalent to it.
        :return: True if this set is equivalent to the other set. False if not.
        :rtype: bool
        """
        pass

    def is_disjoint(self, other: FOLClauseSet) -> bool:
        """ Check if the set is disjoint to the other set

        :param FOLClauseSet other: the other set to be check if this set is disjoint to it.
        :return: True if this set is disjoint to the other set. False if not.
        :rtype: bool
        """
        pass
    
    ######################
    #   Internal Functions
    ######################
    @staticmethod
    def _context_sync(self, a: FOLClauseSet, b: FOLClauseSet):
        """ Syncrhonize both clause set such that they have the same variables internally
        """
        var_a = a._vars
        var_b = b._vars

        vars_set_a = set(a._vars)
        vars_set_b = set(b._vars)
        all_vars = vars_set_a.union(vars_set_b)      

        # go through the symbols in clause to make sure get_symbols() will return consistent node 
        node = b._expr.root
        
    @staticmethod
    def _update_nodes(node: fol_lan.AST_Node, sync_table: dict):
        for child in node.children:
            if isinstance(child, fol_lan.Symbol):
                child = sync_table[child.name]
            else:
                __class__._update_nodes(node=child)


    def _create_context(self, vars):
        context = {}
        for v in vars:
            pass

    def encode(self, solver, vars: list[Var], clause: FOLClause):
        """Encode a first order logic clause into Z3 clauses"""
        # generate symbols in z3
        vars_map = {var.id: solver.get_fresh_variable(var.id, sort=var.type_str) for var in vars}
        # 
        root = clause.root
        z3clause = self._encode(solver=solver, vars_map=vars_map, node=root)
        return z3clause

    def _encode(self, solver, vars_map, node: fol_lan.AST_Node):

        # recursively encode the ast
        if isinstance(node, fol_lan.PropositionNodeBinOp):
            z3_clause1 = self._encode(solver=solver, vars_map=vars_map, node=node.children[0])
            z3_clause2 = self._encode(solver=solver, vars_map=vars_map, node=node.children[1])
            if node.op == "==":
                return solver.clause_equal(z3_clause1, z3_clause2)
            elif node.op == "<=":
                return solver.clause_le(z3_clause1, z3_clause2)
            elif node.op == "<":
                return solver.clause_lt(z3_clause1, z3_clause2)
            elif node.op == ">":
                return solver.clause_gt(z3_clause1, z3_clause2)
            elif node.op == ">=":
                return solver.clause_ge(z3_clause1, z3_clause2)
            elif node.op == "!=":
                return solver.clause_neq(z3_clause1, z3_clause2)
            elif node.op == "&&":
                return solver.clause_and(z3_clause1, z3_clause2)
            elif node.op == "||":
                return solver.clause_or(z3_clause1, z3_clause2)
            elif node.op == "->":
                return solver.clause_implies(z3_clause1, z3_clause2)
            else:
                raise Exception(f"Unsupported operator: {node.op}")

        elif isinstance(node, fol_lan.PropositionNodeUniOp):
            z3_clause = self._encode(solver=solver, vars_map=vars_map, node=node.children[0])
            if node.op == "!":
                return solver.clause_not(z3_clause)
            else:
                raise Exception(f"Unsupported operator: {node.op}")

        elif isinstance(node, fol_lan.PropositionNodeParen):
            return self._encode(solver=solver, vars_map=vars_map, node=node.children[0])
        elif isinstance(node, fol_lan.ExpressionNodeParen):
            return self._encode(solver=solver, vars_map=vars_map, node=node.children[0])
        elif isinstance(node, fol_lan.ExpressionNodeBinOp):
            z3_clause1 = self._encode(solver=solver, vars_map=vars_map, node=node.children[0])
            z3_clause2 = self._encode(solver=solver, vars_map=vars_map, node=node.children[1])
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

