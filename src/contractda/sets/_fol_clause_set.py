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
        solver_instance = self._solver_type()
        vars_map, encoded_clause = self.encode(solver=solver_instance, vars=self._vars, clause=self._expr)
        solver_instance.add_conjunction_clause(encoded_clause)
        ret = solver_instance.check()
        sample = dict()
        if ret == True:
            for var in self._vars:
                solver_var = vars_map[var.id]
                val = solver_instance.get_model_for_var(solver_var)
                if val is not None:
                    sample[var] = val
        else:
            raise Exception("No element available for sample")
        return ret, sample
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

    @classmethod
    def generate_variable_equivalence_constraint_set(cls, vars: list[Var]) -> FOLClauseSet | None:
        if len(vars) <= 1:
            return None
        first_element = fol_lan.Symbol(name=vars[0].id)
        clauses = []
        for var in vars[1:]:
            eq_element = fol_lan.Symbol(name=var.id)
            element_clause1 = FOLClause._create_clause_by_node(first_element)
            element_clause2 = FOLClause._create_clause_by_node(eq_element)
            element_clause1.clause_eq(element_clause2)
            clauses.append(element_clause1)

        # aggregate all the clause sets 
        aggregate_clause = clauses[0]
        for clause in clauses[1:]:
            aggregate_clause.clause_and(clause)

        return cls(vars = vars, expr = aggregate_clause)
    
    @classmethod
    def generate_var_val_equivalence_constraint_set(cls, var: Var, val) -> FOLClauseSet:
        var_element = fol_lan.Symbol(name=var.id)
        val_element = fol_lan.Constant(val = val)
        clause = FOLClause._create_clause_by_node(var_element)
        val_node_clause = FOLClause._create_clause_by_node(val_element)
        clause.clause_eq(val_node_clause)

        return cls(vars = [var], expr = clause)

    @classmethod
    def generate_var_val_gt_constraint_set(cls, var: Var, val) -> FOLClauseSet:
        var_element = fol_lan.Symbol(name=var.id)
        val_element = fol_lan.Constant(val = val)
        clause = FOLClause._create_clause_by_node(var_element)
        val_node_clause = FOLClause._create_clause_by_node(val_element)
        clause.clause_gt(val_node_clause)

        return cls(vars = [var], expr = clause)

    @classmethod
    def generate_var_val_lt_constraint_set(cls, var: Var, val) -> FOLClauseSet:
        var_element = fol_lan.Symbol(name=var.id)
        val_element = fol_lan.Constant(val = val)
        clause = FOLClause._create_clause_by_node(var_element)
        val_node_clause = FOLClause._create_clause_by_node(val_element)
        clause.clause_lt(val_node_clause)

        return cls(vars = [var], expr = clause)
    
    def generate_boundary_set(self, max_depth:int = 3, max_count:int = None, exclude_empty: bool = True) -> tuple[list[ClauseSet], list[ClauseSet]]:
        """Return the boundary set associated with the set

        :param int depth: the depth of traversal in AST
        :param int maximum: maximum number of boundaries searched in both internal and external
        :return: a tuple of a list of internal boundary sets and a list of external boundary sets
        :rtype: tuple[list[ClauseSet], list[ClauseSet]]
        """
        nodes_internal_boundaries, nodes_external_boundaries = self._generate_boundary_set(d = 1, 
                                           max_depth=max_depth, 
                                           node=self.expr.root, 
                                           exclude_empty=exclude_empty,
                                           vars=self.vars)
        internal_boundary_sets = []
        external_boundary_sets = []

        for node in nodes_internal_boundaries:
            internal_boundary_sets.append(FOLClauseSet(vars=self.vars, expr=FOLClause._create_clause_by_node(node)))
        for node in nodes_external_boundaries:
            external_boundary_sets.append(FOLClauseSet(vars=self.vars, expr=FOLClause._create_clause_by_node(node)))

        return internal_boundary_sets, external_boundary_sets
    
    def generate_boundary_set_linear(self, max_count:int = None, exclude_empty: bool = True) -> list[tuple[list[ClauseSet], list[ClauseSet]]]:
        critical_behavior_examples = []
        result = []
        self._generate_boundary_set_linear(result=result, node=self.expr.root, root=self.expr.root, exclude_empty=exclude_empty, vars=self.vars)
        for (in_roots, out_roots) in result:
            example_ins = [FOLClauseSet(vars=self.vars, expr=FOLClause._create_clause_by_node(root)) for root in in_roots] 
            example_outs = [FOLClauseSet(vars=self.vars, expr=FOLClause._create_clause_by_node(root)) for root in out_roots]
            critical_behavior_examples.append((example_ins, example_outs))
        return critical_behavior_examples 
            
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
    @staticmethod
    def _generate_boundary_set(d: int, max_depth: int, node: fol_lan.AST_Node, exclude_empty: bool = False, vars = None) -> tuple[list[fol_lan.AST_Node], list[fol_lan.AST_Node]]:
        # all internal -> internal
        # once external -> external (no need to traverse)
        if d > max_depth:
            neg_node = fol_lan.PropositionNodeUniOp(op="!", exp1=copy.deepcopy(node))
            return ([node], [neg_node])
        
        internal_boundaries: list[fol_lan.AST_Node] = []
        external_boundaries: list[fol_lan.AST_Node] = []

        if isinstance(node, fol_lan.PropositionNodeBinOp):
            if node.op == "==":
                internal_boundaries.append(FOLClauseSet._newnode_change_op(node, op="=="))
                external_boundaries.append(FOLClauseSet._newnode_change_op(node, op="!="))
            elif node.op == "<=":
                internal_boundaries.append(FOLClauseSet._newnode_change_op(node, op="<"))
                internal_boundaries.append(FOLClauseSet._newnode_change_op(node, op="=="))
                external_boundaries.append(FOLClauseSet._newnode_change_op(node, op=">"))
            elif node.op == "<":
                internal_boundaries.append(FOLClauseSet._newnode_change_op(node, op="<"))
                external_boundaries.append(FOLClauseSet._newnode_change_op(node, op="=="))
                external_boundaries.append(FOLClauseSet._newnode_change_op(node, op=">"))    
            elif node.op == ">":
                internal_boundaries.append(FOLClauseSet._newnode_change_op(node, op=">"))
                external_boundaries.append(FOLClauseSet._newnode_change_op(node, op="=="))
                external_boundaries.append(FOLClauseSet._newnode_change_op(node, op="<"))     
            elif node.op == ">=":
                internal_boundaries.append(FOLClauseSet._newnode_change_op(node, op=">"))
                internal_boundaries.append(FOLClauseSet._newnode_change_op(node, op="=="))
                external_boundaries.append(FOLClauseSet._newnode_change_op(node, op="<"))  
            elif node.op == "!=":
                internal_boundaries.append(FOLClauseSet._newnode_change_op(node, op="!="))
                external_boundaries.append(FOLClauseSet._newnode_change_op(node, op="==")) 
            else:
                ch1 = node.children[0]
                ch2 = node.children[1]
                int1, ext1 = FOLClauseSet._generate_boundary_set(d+1, max_depth, ch1)
                int2, ext2 = FOLClauseSet._generate_boundary_set(d+1, max_depth, ch2)
                if node.op == "&&":
                    FOLClauseSet._collect_boundaries(internal_boundaries, int1, int2, op="&&")
                    FOLClauseSet._collect_boundaries(external_boundaries, int1, ext2, op="&&")
                    FOLClauseSet._collect_boundaries(external_boundaries, ext1, int2, op="&&")
                    FOLClauseSet._collect_boundaries(external_boundaries, ext1, ext2, op="&&")
                elif node.op == "||":
                    FOLClauseSet._collect_boundaries(internal_boundaries, int1, int2, op="&&")
                    FOLClauseSet._collect_boundaries(internal_boundaries, int1, ext2, op="&&")
                    FOLClauseSet._collect_boundaries(internal_boundaries, ext1, int2, op="&&")
                    FOLClauseSet._collect_boundaries(external_boundaries, ext1, ext2, op="&&")
                elif node.op == "->":
                    FOLClauseSet._collect_boundaries(internal_boundaries, int1, int2, op="&&")
                    FOLClauseSet._collect_boundaries(external_boundaries, int1, ext2, op="&&")
                    FOLClauseSet._collect_boundaries(internal_boundaries, ext1, int2, op="&&")
                    FOLClauseSet._collect_boundaries(internal_boundaries, ext1, ext2, op="&&") 
                else:
                    raise Exception(f"Unsupported operator: {node.op}")
        elif isinstance(node, fol_lan.PropositionNodeUniOp):
            if node.op == "!":
                ch1 = node.children[0]
                int1, ext1 = FOLClauseSet._generate_boundary_set(d+1, max_depth, ch1)
                internal_boundaries.extend(ext1)
                external_boundaries.extend(int1)
            else:
                raise Exception(f"Unsupported operator: {node.op}")
        else:
            if len(node.children) == 1:
                internal_boundaries, external_boundaries = FOLClauseSet._generate_boundary_set(d, max_depth, node=node.children[0])

        # check emptiness before return...
        if exclude_empty:
            if vars is None:
                err_msg = "Need variables declared to check emptiness of set!"
                LOG.error(err_msg)
                raise Exception(err_msg)
                
            clean_internal_boundaries = []
            clean_external_boundaries = []
            for bound_node in internal_boundaries:
                bound_set = FOLClauseSet(vars=vars, expr=FOLClause._create_clause_by_node(bound_node))
                if bound_set.is_satifiable():
                    clean_internal_boundaries.append(bound_node)

            for bound_node in external_boundaries:
                bound_set = FOLClauseSet(vars=vars, expr=FOLClause._create_clause_by_node(bound_node))
                if bound_set.is_satifiable():
                    clean_external_boundaries.append(bound_node)
            internal_boundaries = clean_internal_boundaries
            external_boundaries = clean_external_boundaries

        return internal_boundaries, external_boundaries
    @staticmethod
    def _generate_boundary_set_linear(result: list[tuple[list[fol_lan.AST_Node], list[fol_lan.AST_Node]]], node: fol_lan.AST_Node, root: fol_lan.AST_Node, exclude_empty: bool = False, vars = None, reverse:bool = False):
        
        #DFS
        in_roots = []
        out_roots = []
        if isinstance(node, fol_lan.PropositionNodeBinOp):
            if node.op == "==":
                FOLClauseSet._newnode_change_op_in_place(node, "!=")
                out_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, "==")
                in_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, "==")
            elif node.op == "<=":
                FOLClauseSet._newnode_change_op_in_place(node, "<")
                in_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, "==")
                in_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, ">")
                out_roots.append(copy.deepcopy(root))   
                FOLClauseSet._newnode_change_op_in_place(node, "<=")
            elif node.op == "<":
                FOLClauseSet._newnode_change_op_in_place(node, "<")
                in_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, "==")
                out_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, ">")
                out_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, "<")    
            elif node.op == ">=":
                FOLClauseSet._newnode_change_op_in_place(node, "<")
                out_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, "==")
                in_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, ">")
                in_roots.append(copy.deepcopy(root))   
                FOLClauseSet._newnode_change_op_in_place(node, ">=") 
            elif node.op == ">":
                FOLClauseSet._newnode_change_op_in_place(node, "<")
                out_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, "==")
                out_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, ">")
                in_roots.append(copy.deepcopy(root))  
                FOLClauseSet._newnode_change_op_in_place(node, ">") 
            elif node.op == "!=":
                FOLClauseSet._newnode_change_op_in_place(node, "==")
                out_roots.append(copy.deepcopy(root))
                FOLClauseSet._newnode_change_op_in_place(node, "!=")
                in_roots.append(copy.deepcopy(root))  
                FOLClauseSet._newnode_change_op_in_place(node, "!=") 
            else:
                left = node.children[0]
                right = node.children[1]
                if node.op == "||":
                    # DFS
                    node.children[1] = fol_lan.PropositionNodeUniOp(op="!", exp1=right)
                    FOLClauseSet._generate_boundary_set_linear(result=result, node=left, root=root, exclude_empty=exclude_empty, vars=vars, reverse=reverse)
                    node.children[1] = right
                    node.children[0] = fol_lan.PropositionNodeUniOp(op="!", exp1=left)
                    FOLClauseSet._generate_boundary_set_linear(result=result, node=right, root=root, exclude_empty=exclude_empty, vars=vars, reverse=reverse)
                    node.children[0] = left
                    # explore different combination
                    in_roots.append(copy.deepcopy(root))
                    node.children[1] = fol_lan.PropositionNodeUniOp(op="!", exp1=right)
                    in_roots.append(copy.deepcopy(root))
                    node.children[0] = fol_lan.PropositionNodeUniOp(op="!", exp1=left)
                    out_roots.append(copy.deepcopy(root))
                    node.children[1] = right
                    in_roots.append(copy.deepcopy(root))
                    node.children[0] = left
                    node.children[1] = right
                    node.children[0] = left
                elif node.op == "&&":
                    # DFS
                    FOLClauseSet._generate_boundary_set_linear(result=result, node=left, root=root, exclude_empty=exclude_empty, vars=vars, reverse=reverse)
                    FOLClauseSet._generate_boundary_set_linear(result=result, node=right, root=root, exclude_empty=exclude_empty, vars=vars, reverse=reverse)
                    # explore different combination
                    in_roots.append(copy.deepcopy(root))
                    node.children[1] = fol_lan.PropositionNodeUniOp(op="!", exp1=right)
                    out_roots.append(copy.deepcopy(root))
                    node.children[0] = fol_lan.PropositionNodeUniOp(op="!", exp1=left)
                    out_roots.append(copy.deepcopy(root))
                    node.children[1] = right
                    out_roots.append(copy.deepcopy(root))
                    node.children[0] = left
                    node.children[1] = right
                    node.children[0] = left
                elif node.op == "->":
                    # DFS
                    node.children[1] = fol_lan.PropositionNodeUniOp(op="!", exp1=right)
                    FOLClauseSet._generate_boundary_set_linear(result=result, node=left, root=root, exclude_empty=exclude_empty, vars=vars, reverse=reverse^True)
                    node.children[1] = right
                    FOLClauseSet._generate_boundary_set_linear(result=result, node=right, root=root, exclude_empty=exclude_empty, vars=vars, reverse=reverse)
                    # explore different combination
                    in_roots.append(copy.deepcopy(root))
                    node.children[1] = fol_lan.PropositionNodeUniOp(op="!", exp1=right)
                    out_roots.append(copy.deepcopy(root))
                    node.children[0] = fol_lan.PropositionNodeUniOp(op="!", exp1=left)
                    in_roots.append(copy.deepcopy(root))
                    node.children[1] = right
                    in_roots.append(copy.deepcopy(root))
                    node.children[0] = left
                    node.children[1] = right
                    node.children[0] = left
                else:
                    raise Exception(f"Unsupported operator: {node.op}")
        elif isinstance(node, fol_lan.PropositionNodeUniOp):
            if node.op == "!":
                ch = node.children[0]
                # flip the 
                FOLClauseSet._generate_boundary_set_linear(result=result, node=ch, root=root, exclude_empty=exclude_empty, vars=vars, reverse=(reverse ^ True))
                out_roots.append(copy.deepcopy(root))
                node.children[0] = fol_lan.PropositionNodeUniOp(op="!", exp1=ch)
                in_roots.append(copy.deepcopy(root))
                node.children[0] = ch
            else:
                raise Exception(f"Unsupported operator: {node.op}")
        else:
            if len(node.children) == 1:
                FOLClauseSet._generate_boundary_set_linear(result=result, node=node.children[0], root=root, exclude_empty=exclude_empty, vars=vars, reverse=reverse)
                return
        if reverse:
            result.append((out_roots, in_roots))
        else:
            result.append((in_roots, out_roots))

        return
        
    
    @staticmethod
    def _newnode_change_op_in_place(node: fol_lan.AST_Node, op:str) -> fol_lan.AST_Node:
        node.op = op
        return   
    
    @staticmethod
    def _newnode_change_op(node: fol_lan.AST_Node, op:str) -> fol_lan.AST_Node:
        new_node = copy.deepcopy(node)
        new_node.op = op
        return new_node
    
    @staticmethod
    def _collect_boundaries(boundaries: list[fol_lan.AST_Node], bounds_a: list[fol_lan.AST_Node], bounds_b: list[fol_lan.AST_Node], op: str):
        for bound_a in bounds_a:
            for bound_b in bounds_b:
                new_bound_a = copy.deepcopy(bound_a)
                new_bound_b = copy.deepcopy(bound_b)
                boundaries.append(fol_lan.PropositionNodeBinOp(op=op, exp1 = new_bound_a, exp2=new_bound_b))





        