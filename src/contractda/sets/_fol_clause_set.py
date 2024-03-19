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
    def __init__(self, vars: ClauseSetVarType, expr: str | FOLClause, ctx = None):
        """ clause_type: the """
        # create the context
        if isinstance(expr, str):
            expr = FOLClause(description = expr, ctx = ctx)
        
        self._expr = expr
        # check if the variables are indeed mentioned in expr
        context_ok, failed_list = self._check_context(vars = vars, expr=self._expr)
        if not context_ok:
            raise Exception(f"Variables {failed_list} not specified in the description: {expr}")
        # store the 
        self._vars = vars
        # solver
        self._solver_type = Z3Interface
        pass

    def __str__(self):
        return str(self.expr)
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

    def project(self, vars: Iterable[Var], is_refine: bool = True, simplify = True) -> FOLClauseSet:
        """ Projection opration on set 

        :param vars: the list of variables to be the projection result.
        :param bool is_refine: whether the projection is to result in refinement or abstraction
        :param bool simplify: whether the clause should be simplilfy
        :return: A new set which represents the Projection of the set on the input variables
        :rtype: FOLClauseSet
        """
        # check the variables are OK.
        var_set = set(self._vars)
        target_var_set = set(vars)
        self._verify_unique_vars(var_set.union(target_var_set))
        solver_instance = self._solver_type()
        vars_map, encoded_clause = self.encode(solver=solver_instance, vars=self._vars, clause=self._expr)

        # find the eliminated vars
        eliminated_vars = var_set.difference(target_var_set)
        solver_vars = [vars_map[var.id] for var in eliminated_vars]

        # quantifier elimination
        ret = ""
        if is_refine:
            q_clause = solver_instance.clause_forall(solver_vars, encoded_clause)
        else:
            q_clause = solver_instance.clause_exists(solver_vars, encoded_clause)
        LOG.debug(f"Attempting Qunatifier Elimination: {q_clause}")
        try:
            ret = solver_instance.quantify_elimination(q_clause)
        except:
            LOG.ERROR("Quantifier Elimination Failed")
        LOG.debug(f"Quantifier Elimination Success: {ret}")
        # TODO: the syntex seems to be different
        if simplify:
            LOG.debug(f"Attempting Clause Simplify: {q_clause}")
            ret = solver_instance.simplify_clause(ret)
            LOG.debug(f"Clause Simplify: {ret}")
        return self.__class__(vars=vars, expr=str(ret))

    def is_contain(self, element: dict) -> bool:
        """ Check if the set is contain the element

        :param element: A dictionary that maps variable to its values
        :return: True if the element is in the set. False if not.
        :rtype: bool
        """
        # if dictionary is using id
        if element:
            sample = list(element.keys())[0]
            if isinstance(sample, str):
                value_table = {var: val for var, val in element.items()}
            elif isinstance(sample, Var):
                value_table = {var.id: val for var, val in element.items()}
            else:
                raise Exception("Unsupported element type")
            # empty table
        # create value_table
        return self._expr.evaluate(value_table=value_table)

    def is_subset(self, other: FOLClauseSet) -> bool:
        """ Check if the set is a subset of the other set

        :param FOLClauseSet other: the other set to be check if this set is a subset of it.
        :return: True if this set is a subset of the other set. False if not.
        :rtype: bool
        """
        LOG.debug(f"Checking if {self} is a subset of {other}")
        try:
            new_vars = self._combine_vars(self._vars, other._vars)
        except:
            LOG.error("The two set is defined under different variables with the same identifier!")
        # if a and not b is unsatisfiable, then a is a subset ( there is no element in a but not in b i.e., all element is in b)
        new_expr_a = copy.deepcopy(self.expr)
        new_expr_b = copy.deepcopy(other.expr)

        new_expr_a.clause_and(new_expr_b.clause_not())
        ret = not self._clause_satisfiable(vars=new_vars, clause=new_expr_a)
        LOG.debug(f"Result: {ret}")

        return ret

    def is_proper_subset(self, other: FOLClauseSet) -> bool:
        """ Check if the set is a proper subset of the other set

        :param FOLClauseSet other: the other set to be check if this set is a proper subset of it.
        :return: True if this set is a proper subset of the other set. False if not.
        :rtype: bool
        """
        return self.is_subset(other=other) and not other.is_subset(other=self)

    def is_satifiable(self) -> bool:
        """ Check if the set is satisfiable, i.e., not empty

        :return: True if this set is satisfiable. False if not.
        :rtype: bool
        """
        return self._clause_satisfiable(vars=self._vars, clause=self._expr)

    def is_equivalence(self, other: FOLClauseSet) -> bool:
        """ Check if the set is equivalent to the other set

        :param FOLClauseSet other: the other set to be check if this set is equivalent to it.
        :return: True if this set is equivalent to the other set. False if not.
        :rtype: bool
        """
 
        try:
            new_vars = self._combine_vars(self._vars, other._vars)
        except:
            LOG.error("The two set is defined under different variables with the same identifier!")
        
        # find counter example of a and not b or b and not a
        # we must show that it is unsat
        # TODO: this can be more efficient as the generated expression do not used outside: it can be not a tree (share the subtrees)
        # a -> b
        new_expr1 = copy.deepcopy(self.expr)
        new_expr_b1 = copy.deepcopy(other.expr)
        new_expr1.clause_and(new_expr_b1.clause_not())
        # b -> a
        new_expr_a2 = copy.deepcopy(self.expr)
        new_expr2 = copy.deepcopy(other.expr)
        new_expr2.clause_and(new_expr_a2.clause_not())
        # a -> b and b -> a
        new_expr1.clause_or(new_expr2)
        
        return not self._clause_satisfiable(vars=new_vars, clause=new_expr1)

    def is_disjoint(self, other: FOLClauseSet) -> bool:
        """ Check if the set is disjoint to the other set

        :param FOLClauseSet other: the other set to be check if this set is disjoint to it.
        :return: True if this set is disjoint to the other set. False if not.
        :rtype: bool
        """
        try:
            new_vars = self._combine_vars(self._vars, other._vars)
        except:
            LOG.error("The two set is defined under different variables with the same identifier!")
        # find counter example that a and b (there should not be any element in both set)
        new_expr_a = copy.deepcopy(self.expr)
        new_expr_b = copy.deepcopy(other.expr)

        new_expr_a.clause_and(new_expr_b)

        return not self._clause_satisfiable(vars=new_vars, clause=new_expr_a)
    
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


    def _clause_satisfiable(self, vars: list[Var], clause: FOLClause):
        solver_instance = self._solver_type()
        _, encoded_clause = self.encode(solver=solver_instance, vars=vars, clause=clause)
        solver_instance.add_conjunction_clause(encoded_clause)
        ret = solver_instance.check()
        return ret   

    def encode(self, solver, vars: list[Var], clause: FOLClause, vars_map: dict | None = None):
        """Encode a first order logic clause into solver clauses"""
        # generate symbols in solver
        if vars_map is None:
            vars_map = {var.id: solver.get_fresh_variable(var.id, sort=var.type_str) for var in vars}
        # 
        root = clause.root
        solver_clause = self._encode(solver=solver, vars_map=vars_map, node=root)
        return vars_map, solver_clause

    def _encode(self, solver, vars_map, node: fol_lan.AST_Node):

        # recursively encode the ast
        if isinstance(node, fol_lan.PropositionNodeBinOp):
            solver_clause1 = self._encode(solver=solver, vars_map=vars_map, node=node.children[0])
            solver_clause2 = self._encode(solver=solver, vars_map=vars_map, node=node.children[1])
            if node.op == "==":
                return solver.clause_equal(solver_clause1, solver_clause2)
            elif node.op == "<=":
                return solver.clause_le(solver_clause1, solver_clause2)
            elif node.op == "<":
                return solver.clause_lt(solver_clause1, solver_clause2)
            elif node.op == ">":
                return solver.clause_gt(solver_clause1, solver_clause2)
            elif node.op == ">=":
                return solver.clause_ge(solver_clause1, solver_clause2)
            elif node.op == "!=":
                return solver.clause_neq(solver_clause1, solver_clause2)
            elif node.op == "&&":
                return solver.clause_and(solver_clause1, solver_clause2)
            elif node.op == "||":
                return solver.clause_or(solver_clause1, solver_clause2)
            elif node.op == "->":
                return solver.clause_implies(solver_clause1, solver_clause2)
            else:
                raise Exception(f"Unsupported operator: {node.op}")

        elif isinstance(node, fol_lan.PropositionNodeUniOp):
            solver_clause = self._encode(solver=solver, vars_map=vars_map, node=node.children[0])
            if node.op == "!":
                return solver.clause_not(solver_clause)
            else:
                raise Exception(f"Unsupported operator: {node.op}")

        elif isinstance(node, fol_lan.PropositionNodeParen):
            return self._encode(solver=solver, vars_map=vars_map, node=node.children[0])
        elif isinstance(node, fol_lan.ExpressionNodeParen):
            return self._encode(solver=solver, vars_map=vars_map, node=node.children[0])
        elif isinstance(node, fol_lan.ExpressionNodeBinOp):
            solver_clause1 = self._encode(solver=solver, vars_map=vars_map, node=node.children[0])
            solver_clause2 = self._encode(solver=solver, vars_map=vars_map, node=node.children[1])
            if node.op == "+":
                return solver_clause1 + solver_clause2
            elif node.op == "-":
                return solver_clause1 - solver_clause2
            elif node.op == "*":
                return solver_clause1 * solver_clause2
            elif node.op == "/":
                return solver_clause1 / solver_clause2
            elif node.op == "^":
                return solver_clause1 ** solver_clause2
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
            solver_var = vars_map.get(id, None)
            if solver_var is None:
                raise Exception(f"Not specified varibles {id}") 
            
            return solver_var

