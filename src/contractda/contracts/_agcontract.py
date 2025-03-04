import copy

from contractda.contracts._contract_base import ContractBase
from contractda.sets import SetBase, FOLClauseSet, ExplicitSet
from contractda.vars import Var
from contractda.solvers import SolverInterface
from contractda.sets._fol_lan import name_remap

from contractda.logger._logger import LOG

class AGContract(ContractBase):
    """Class for Assume-Guarantee Contract (AG Contract)

    An assume-guarnatee contract defines the contract by assumption and guarantee.
    The assumption is the environment where the system is expected to work.
    The guarantee is the result ensured by the system if the assumption holds
    """

    def __init__(self, vars: list[Var], assumption: SetBase | str, guarantee: SetBase | str, language = "FOL"):
        """Constructor

        :param list[Var] vars: the variables
        :param SetBase|str constraint: the constraint
        :param SetBase|str behavior: the intrinsic behavior
        """
        self._assumption: SetBase = self._convert_to_sets_based_on_language(vars, assumption, language)
        self._guarantee: SetBase = self._convert_to_sets_based_on_language(vars, guarantee, language)
        self._vars: list[Var] = vars
        self._assigned_input_vars: list[Var] = None

    def __str__(self):
        return f" AG Contract: Assumption: {self.assumption}, Guarantee: {self.guarantee}"
    @property
    def assumption(self) -> SetBase:
        """The constraint of the """
        return self._assumption
    
    @property
    def guarantee(self) -> SetBase:
        return self._guarantee
    
    @property
    def vs(self) -> list[Var]:
        return self._vars
    
    @property
    def input_var_symbols(self) -> list[Var]:
        """The input vars as if the contarct is defined with inputs and outputs"""
        if self._assigned_input_vars:
            return {v.id for v in self._assigned_input_vars}
        else:
            # default choice, directly use symbols from assumption
            return self._assumption.expr.get_symbols()
        
    @property
    def input_var(self) -> list[Var]:
        """The input vars as if the contarct is defined with inputs and outputs"""
        if self._assigned_input_vars:
            return self._assigned_input_vars
        else:
            # default choice, directly use symbols from assumption
            symbols = self._assumption.expr.get_symbols()
            return [v for v in self.vs if v.id in symbols]

    
    @property
    def environment(self) -> SetBase:
        """ The targeted environment specified by the contracts"""
        return self.assumption
    
    @property
    def implementation(self) -> SetBase:
        """ The allowed implementation specified by the contracts"""
        return self.guarantee.union(self.assumption.complement())
    
    @property
    def assumption_vs(self) -> list[Var]:
        symbols = self.input_var_symbols
        return [v for v in self.vs if v.id in symbols]
    
    @property
    def non_assumption_vs(self) -> list[Var]:
        assumption_symbols = self.input_var_symbols
        return [v for v in self.vs if v.id not in assumption_symbols]        
    
    @property
    def obligation(self) -> SetBase:
        """ The contract obligation, see Beneviste et al. Multiple Viewpoint Contract-Based Specification and Design, FMCO07"""
        return self.guarantee.intersect(self.assumption)


    def add_constraint(self, constraint: SetBase, adjusted_input: list[Var] = None):
        """ Impose constraints on both assumption and guarantee"""
        if constraint is None:
            return 
        self._assumption = self._assumption.intersect(constraint)
        self._guarantee = self._guarantee.intersect(constraint)
        self._vars = self._guarantee.vars # determine vars 
        self._assigned_input_vars = adjusted_input # determine introduced input variables

    ##################################
    #   Contract Query with Inputs
    ##################################
    def check_environment_satisfy(self, env: SetBase) -> bool:
        return not env.intersect(self.assumption.complement()).is_satifiable()

    ##################################
    #   Contract Property
    ##################################
    def is_receptive(self, solver: SolverInterface = None) -> bool:
        """ Whether the contract is recptive

        Receptive means for each targeted environment, there is a allowed behavior.

        :return: True if the contract is receptive, False if not
        :rtype: bool
        """
        # Check if there is counter example: some element satisfies A but has no corresponding behavior allowed by G
        # (A && ! Exists(v not in A, G))

        
        if isinstance(self.guarantee, FOLClauseSet):
            if solver is None:
                solver = self.assumption._solver_type()
            # ensure all variables are encoded
            vars_map = {v.id: solver.get_fresh_variable(v.id, sort=v.type_str) for v in self.vs}
            # encode both guarantee and assumption
            var_map, encoded_guarantee = self.guarantee.encode(solver=solver, vars=self.guarantee.vars, clause=self.guarantee.expr, vars_map=vars_map)
            var_map, encoded_assumption = self.assumption.encode(solver=solver, vars=self.assumption.vars, clause=self.assumption.expr, vars_map=vars_map)
            # prepare quantifier variables
            exist_vs = [var_map[v.id] for v in self.non_assumption_vs]
            # form the clause for checking
            if exist_vs:
                encoded_clause = solver.clause_and(encoded_assumption, 
                                                solver.clause_not(
                                                    solver.clause_exists(exist_vs, encoded_guarantee)))
            else:
                #empty due to same variables in assumption and guarantee
                encoded_clause = solver.clause_and(encoded_assumption, 
                                                solver.clause_not(encoded_guarantee))
            # solve the existencde
            solver.add_conjunction_clause(encoded_clause)
            exist_counter_example = solver.check()
            return not exist_counter_example  
        elif isinstance(self.guarantee, ExplicitSet):
            # Explicit set
            # find the counter example that if there is a input without behavior
            # we can use projection to achieve this
            legal_env = self.guarantee.project(self.assumption.ordered_vars, is_refine=False)
            ret = self.assumption.is_subset(legal_env)
            return ret
        else:
            raise NotImplementedError

    def is_compatible(self) -> bool:
        """ Whether the contract is compatible

        A contract is compatible if the implementation set is not empty
        Receptive means for each targeted environment, there is a allowed behavior.

        :return: True if the contract is compatible, False if not
        :rtype: bool
        """
        return self.implementation.is_satifiable()

    def is_consistent(self) -> bool:
        """ Whether the contract is consistent

        A contract is consistent if the environment set is not empty

        :return: True if the contract is consistent, False if not
        :rtype: bool
        """
        return self.environment.is_satifiable()
    ##################################
    #   Contract Operations
    ##################################

    def composition(self, other: ContractBase) -> ContractBase:
        """ Generate the contract for the system consisting of this contract and the other contract

        Given subsystem contract a and b, composition find the system contract c such that c is satisfied if and only if both subsystem satisfy their contracts.
        This method will update the contract of itself inplace.

        :param ContractBase other: the other contract to be composed with this contract
        :return: the composition result
        :rtype: ContractBase
        """
        a1 = self.environment
        a2 = other.environment
        g1 = self.implementation
        g2 = other.implementation

        
        ret_g = g1.intersect(g2)
        ret_a = a1.intersect(a2).union(ret_g.complement())

        return AGContract(vars=self.vs, assumption=ret_a, guarantee=ret_g)
    
    def quotient(self, other: ContractBase):
        """ Finding missing component contracts in the system

        Given system contract a, subsystem contract b, the quotient finds the contract c such that c compose b equals a
        This method will update the contract of itself inplace.

        :param ContractBase other: the known subsystem contract
        :return: the quotient result 
        :rtype: ContractBase
        """
        a1 = self.environment
        a2 = other.environment
        g1 = self.implementation
        g2 = other.implementation

        ret_a = a1.intersect(g2)
        ret_g = a2.intersect(g1).union(ret_a.complement())

        return AGContract(vars=self.vs, assumption=ret_a, guarantee=ret_g)

    def conjunction(self, other: ContractBase):
        """ Combining different condition contracts

        Given system condition contract a and b, the conjunction finds the contract c such that c is satisfied if and only if either a or b is satisfied
        This method will update the contract of itself inplace.

        :param ContractBase other: the other contract to perform conjunction with this contract
        :return: the conjunction result
        :rtype: ContractBase
        """
        a1 = self.environment
        a2 = other.environment
        g1 = self.implementation
        g2 = other.implementation

        ret_a = a1.union(a2)
        ret_g = g1.intersect(g2)

        return AGContract(vars=self.vs, assumption=ret_a, guarantee=ret_g)

    def implication(self, other: ContractBase):
        """ Finding the missing condition

        Given system contract a and know condition contract b, the implication finds the contract c such that the conjunction of b and c becomes a
        This method will update the contract of itself inplace.

        :param ContractBase other: the other contract to perform implication with this contract
        :return: the implication result
        :rtype: ContractBase
        """
        a1 = self.environment
        a2 = other.environment
        g1 = self.implementation
        g2 = other.implementation

        ret_g = g2.union(g1.complement())
        ret_a = a2.intersect(a1.complement()).union(ret_g.complement())
        

        return AGContract(vars=self.vs, assumption=ret_a, guarantee=ret_g)

    def merging(self, other: ContractBase):
        """ Combining different viewpoint contracts

        Given system viewpoint contract a and b, the mergin finds the contract c such that c is satisfied if and only if either a or b is satisfied
        This method will update the contract of itself inplace.

        :param ContractBase other: the other contract to perform conjunction with this contract
        :return: the merging result
        :rtype: ContractBase
        """
        a1 = self.environment
        a2 = other.environment
        g1 = self.implementation
        g2 = other.implementation

        ret_a = a1.intersect(a2)
        ret_g = g1.intersect(g2).union(ret_a.complement())

        return AGContract(vars=self.vs, assumption=ret_a, guarantee=ret_g)


    def separation(self, other: ContractBase):
        """ Combining different viewpoint contracts

        Given system contract a and know viewpoint contract b, the implication finds the contract c such that the merging of b and c becomes a
        This method will update the contract of itself inplace.

        :param ContractBase other: the other contract to perform implication with this contract
        :return: the separation result
        :rtype: ContractBase
        """
        a1 = self.environment
        a2 = other.environment
        g1 = self.implementation
        g2 = other.implementation

        ret_g = a2.intersect(g1)
        ret_a = a1.intersect(g2).union(ret_g.complement())

        return AGContract(vars=self.vs, assumption=ret_a, guarantee=ret_g)

    def saturation(self) -> ContractBase:
        """Saturate the contract"""
        # C union (not B)
        return AGContract(vars=self.vs, assumption=self.environment, guarantee=self.implementation)


    ##################################
    #   Contract Relations
    ##################################
    def is_refined_by(self, other: ContractBase) -> bool:
        """ Whether the contract is refined by the other contract

        A contract is refined by the other contract if the all the implementations of the new contract satisfy the original contract 
        and they can work under the environment required by the original contract.

        :param ContractBase others: all the subsystem contracts of :py:class:`~contract.contracts.ContractBase` 
        :return: True if the contract is refined by the others, False if not
        :rtype: bool
        """

        # saturation does not matter for CB contract or AG contract
        # TODO: prevent saturation if it is already saturated and flagged
        a1 = self.environment
        a2 = other.environment
        g1 = self.implementation
        g2 = other.implementation

        return a1.is_subset(a2) and g2.is_subset(g1)

    def is_conformed_by(self, other: ContractBase) -> bool:
        """Whether the contract is conformed by the other contract
        
        A contract is conformed by the other contract if the obligation of the other contract is contained by the original contract's obligation.
    
        :param ContractBase others: all the subsystem contracts of :class:`~contract.contracts.ContractBase` 
        :return: True if the contract is conformed by the others, False if not
        :rtype: bool
        """
        return other.obligation.is_subset(self.obligation)

    def is_strongly_dominated_by(self, other: ContractBase) -> bool:
        """Whether the contract is strongly dominated by the other contract
        
        Strong dominated mean both refined and conformed by the other contract.

        :param ContractBase others: all the subsystem contracts of :class:`~contract.contracts.ContractBase` 
        :return: True if the contract is strongly dominated by the others, False if not
        :rtype: bool
        """
        return self.is_conformed_by(other) and self.is_refined_by(other)

    def is_strongly_replaceable_by(self, other: ContractBase, solver: SolverInterface = None) -> bool:
        """ Check if the contract is strongly replaceable by the other contract

        Contract A is strongly replaceable by contract B if contract B has behavior for all targeted environment of A.

        Strong replaceability is an important property to verify no vacuous design under independent design.
        Strong replaeability is transitive, i.e. if A is strongly replaceable by B, and B is strongly replacceable by C, 
        then A is strongly replaceable by C. 
        When a series of single contract refinement holds the strong replaceability for each contract refinement, 
        the final one must strongly replace the original system contract and thus we can implementation a design that is not vacuous.

        :param ContractBase other: the other contract to be checked if it strongly replaces this contract
        :return: True if the contract is strongly replaceable by the other, False if not
        :rtype: bool
        """
        # Check if there is counter example: some element satisfies A1 but has no corresponding behavior allowed by G2
        # (A! && ! Exists(v not in A1, G2))
        
        if isinstance(other.guarantee, FOLClauseSet):
            if solver is None:
                solver = self.assumption._solver_type()
            # ensure all variables are encoded
            vars_map = {v.id: solver.get_fresh_variable(v.id, sort=v.type_str) for v in self.vs}
            # encode both guarantee and assumption
            var_map, encoded_guarantee = other.guarantee.encode(solver=solver, vars=other.guarantee.vars, clause=other.guarantee.expr, vars_map=vars_map)
            var_map, encoded_assumption = self.assumption.encode(solver=solver, vars=self.assumption.vars, clause=self.assumption.expr, vars_map=vars_map)
            # prepare quantifier variables
            exist_vs = [var_map[v.id] for v in self.non_assumption_vs]
            # form the clause for checking
            if exist_vs:
                encoded_clause = solver.clause_and(encoded_assumption, 
                                                solver.clause_not(
                                                    solver.clause_exists(exist_vs, encoded_guarantee)))
            else:
                #empty due to same variables in assumption and guarantee
                encoded_clause = solver.clause_and(encoded_assumption, 
                                                solver.clause_not(encoded_guarantee))
            # solve the existencde
            solver.add_conjunction_clause(encoded_clause)
            exist_counter_example = solver.check()
            return not exist_counter_example  
        elif isinstance(other.guarantee, ExplicitSet):
            # Explicit set
            # find the counter example that if there is a input without behavior
            # we can use projection to achieve this
            #print(other.guarantee.ordered_expr)
            legal_env = other.guarantee.project(self.assumption.ordered_vars, is_refine=False)
            ret = self.assumption.is_subset(legal_env)
            return ret
        else:
            raise NotImplementedError()

    def is_replaceable_by(self, other: ContractBase, solver: SolverInterface = None) -> bool:
        """ Check if the contract is replaceable by the other contract

        Contract A is replaceable by contract B if contract B has behavior under some targeted environment of A.

        Replaceability is an important property to ensure we can implementation a nonvacuous design of the original contract based on the refined contract.

        :param ContractBase other: the other contract to be checked if it replaces this contract
        :return: True if the contract is strongly replaceable by the other, False if not
        :rtype: bool
        """
        # Check if there is a positive example: exist some element satisfies A1 and has corresponding behavior allowed by G2
        # (A! && ! Exists(v not in A1, G2))

        
        if isinstance(other.guarantee, FOLClauseSet):
            if solver is not None:
                raise NotImplementedError("I have not implement user specified solver for internal set operation")
            return self.assumption.intersect(other.guarantee).is_satifiable()
        elif isinstance(other.guarantee, ExplicitSet):
            legal_env = other.guarantee.project(self.assumption.ordered_vars, is_refine=False)
            ret = self.assumption.intersect(legal_env).is_satifiable()
            return ret
        else:
            raise NotImplementedError()

    def is_independent_decomposition_of(self, other1: ContractBase, other2: ContractBase) -> bool:
        """ Check if the contract decomposition can allowed independent receptive refinement without causing vacuous design.

        TO BE ADDED (new contribution)

        :param ContractBase other1: one of the decomposition contract
        :param ContractBase other2: one of the decomposition contract
        :return: True if the contract is refined by other, False if not
        :rtype: bool
        """
        # Given contract Cs, C1, C2 all of them are receptive contracts and C1 compose C2 refines Cs
        # step 1: find type 1 fixed points, check if all targeted environment has a type 1 contract 
        # A1 * G1 * A2 * G2 is the set of all fixed points
        # formulation of type 1: An element ef in the fixed point set such that for any e such that project(I1)(ef) * G1 only contains ef
        #                         
        #                                           and for any e such that project(I2)(ef) * G2 only contains ef
        LOG.debug(f"===================================================")
        LOG.debug(f"=            Independent Design Check             =")
        LOG.debug(f"===================================================")
        LOG.debug(f"[INDE] Check Variables")
        # find common variables 


        ret = True
        failed_env = []
        if isinstance(self.guarantee, ExplicitSet):
            related_inputs_1 = set(other1.assumption.vars).difference(set(self.assumption.vars))
            LOG.debug(f"[INDE] Related inputs 1: {[var.id for var in related_inputs_1]}")
            related_inputs_2 = set(other2.assumption.vars).difference(set(self.assumption.vars))
            LOG.debug(f"[INDE] Related inputs 2: {[var.id for var in related_inputs_2]}")
            related_inputs = list(related_inputs_1.union(related_inputs_2))
            related_inputs = sorted(related_inputs, key = lambda var: var.id)
            LOG.debug(f"[INDE] Related inputs: {[var.id for var in related_inputs]}")

            # # this is debug
            # type_1_fixed_points = [] # forall (e of fresh all variables!), (e \in project(I1)(ef) and G1 and e == ef)
            # type_2_fixed_points = []
            # type_3_fixed_points = []
            # LOG.debug(f"[INDE] All fixed point: {all_fixed_points}")
            # for ef in all_fixed_points:
            #     # form project(I1)(ef) and G1
            #     LOG.debug(f"[INDE] Checking fixed point {ef}")
            #     ef_set = ExplicitSet(self.vs, expr=[ef])
            #     neighbor_behaviors_1 = ef_set.project(other1.assumption.ordered_vars, is_refine=False).intersect(other1.guarantee)
            #     neighbor_behaviors_1.reorder_vars(self.vs)
            #     LOG.debug(f"[INDE] Possible behaviors for C1 {neighbor_behaviors_1}")
            #     neighbor_behaviors_2 = ef_set.project(other2.assumption.ordered_vars, is_refine=False).intersect(other2.guarantee)
            #     neighbor_behaviors_2.reorder_vars(self.vs)
            #     LOG.debug(f"[INDE] Possible behaviors for C2 {neighbor_behaviors_2}")
            #     if ef_set.is_equivalence(neighbor_behaviors_1) and ef_set.is_equivalence(neighbor_behaviors_2):
            #         LOG.debug(f"[INDE] {ef} is a type 1 fixed point")
            #         type_1_fixed_points.append(ef)
            #     else:
            #         LOG.debug(f"[INDE] {ef} is not a type 1 fixed point")
            #         if neighbor_behaviors_1.is_subset(all_fixed_points) and neighbor_behaviors_2.is_subset(all_fixed_points):
            #             LOG.debug(f"[INDE] {ef} is a type 3 fixed point")
            #             type_3_fixed_points.append(ef)
            #         else:
            #             LOG.debug(f"[INDE] {ef} is a type 2 fixed point")
            #             type_2_fixed_points.append(ef)

            # LOG.debug(f"[INDE] Type 1 Fixed point: {[elem for elem in type_1_fixed_points]}")
            # LOG.debug(f"[INDE] Type 2 Fixed point: {[elem for elem in type_2_fixed_points]}")
            # LOG.debug(f"[INDE] Type 3 Fixed point: {[elem for elem in type_3_fixed_points]}")

            # real useful way to quickly identify - direclty start the search in the graph
            for env in self.assumption.internal_expr:
                LOG.debug(f"[INDE] Checking environment: {[var.id for var in self.assumption.internal_vars]} = {env}")
                env_set = ExplicitSet(self.assumption.internal_vars, [env])
                all_fixed_points = other1.obligation.intersect(other2.obligation).intersect(env_set) # only consider the targeted env
                all_fixed_points = all_fixed_points.project(list(related_inputs)).internal_expr

                possible_fixed_point = []
                candidates = set(copy.copy(all_fixed_points))
                while candidates:
                    LOG.debug(f"[INDE] Candidates: {candidates}")
                    dirty_flag = False
                    test_root = candidates.pop()
                    LOG.debug(f"[INDE] Start Fixed point group search for {test_root}")
                    group = [test_root]
                    is_dirty = self._explored_fixed_point_explicit(other1, other2, explored_point=test_root, group=group, all_fixed_points=all_fixed_points, related_inputs=related_inputs, env_set=env_set)
                    if not is_dirty:
                        possible_fixed_point.extend(group)
                        LOG.debug(f"[INDE] Add possible fixed points: {possible_fixed_point}")
                    candidates = candidates - set(group)
                if possible_fixed_point:
                    LOG.debug(f"[INDE] Exist possible fixed points: {possible_fixed_point}")
                else:
                    LOG.debug(f"[INDE] No possible fixed points for environement {[var.id for var in self.assumption.internal_vars]} = {env}")
                    failed_env.append(env)
                    ret = False
                    
        elif isinstance(self.guarantee, FOLClauseSet):
            ret = self._is_independent_decomposition_of_infinite_set(other1=other1, other2=other2, dmax = 10)

        LOG.debug(f"===================================================")
        LOG.debug(f"=            Independent Design Result            =")
        LOG.debug(f"===================================================")
        LOG.debug(f"Result: {ret}")
        if ret == True:
            LOG.debug(f"[INDE] Positive proved")
            return ret
        elif ret == False:
            LOG.debug(f"[INDE] Negative proved")
            return ret
        else:# unkno
            LOG.debug(f"[INDE] Unknown, dmax exceeds!")
            return False
    
    def _is_independent_decomposition_of_infinite_set(self, other1: ContractBase, other2: ContractBase, dmax = 5, dinit = 1) -> bool:

        # find related inputs
        LOG.debug(f"[INDE] Determining the port partition....")
        all_var = set(self.vs).union(set(other1.vs)).union(set(other2.vs))
        a1_var = other1.input_var_symbols
        a2_var = other2.input_var_symbols
        as_var = self.input_var_symbols
        
        related_inputs_1 = a1_var.difference(as_var)
        related_inputs_1 = set([v for v in all_var if v.id in related_inputs_1])
        LOG.debug(f"[INDE] Related inputs 1: {[var.id for var in related_inputs_1]}")
        related_inputs_2 = a2_var.difference(as_var)
        related_inputs_2 = set([v for v in all_var if v.id in related_inputs_2])
        LOG.debug(f"[INDE] Related inputs 2: {[var.id for var in related_inputs_2]}")
        related_inputs = list(related_inputs_1.union(related_inputs_2))
        related_inputs = sorted(related_inputs, key = lambda var: var.id)
        LOG.debug(f"[INDE] Related ports: {[var.id for var in related_inputs]}")

        system_inputs = [v for v in all_var if v.id in as_var]
        inde_outputs = all_var.difference(related_inputs).difference(system_inputs)
        LOG.debug(f"[INDE] Distinct Ouputs: {[var.id for var in inde_outputs]}")

        all_vars_except_env = list(related_inputs) + list(inde_outputs)
        #solver and their vars
        solver = self.assumption._solver_type()
        vars_map = {v.id: solver.get_fresh_variable(v.id, sort=v.type_str) for v in all_var}
        solver_var_related_inputs = [vars_map[v.id] for v in related_inputs]
        solver_var_distinct_outputs = [vars_map[v.id] for v in inde_outputs]
        all_vars_except_env_solver = [vars_map[v.id] for v in all_vars_except_env]

        # some clauses
        
        all_fixed_points = other1.obligation.intersect(other2.obligation).intersect(self.assumption)
        vars_map, encoded_assumption = self.assumption.encode(solver=solver, vars=self.assumption.vars, clause=self.assumption.expr, vars_map=vars_map)
        vars_map, encoded_all_fp = all_fixed_points.encode(solver=solver, vars=all_fixed_points.vars, clause=all_fixed_points.expr, vars_map=vars_map)
        # the all fixed points should eliminate distinct output
        if solver_var_distinct_outputs:
            encoded_all_fp_copied = solver.clause_exists(solver_var_distinct_outputs, encoded_all_fp)

        #copy 
        related_input_array = [related_inputs]
        distinct_output_array = [inde_outputs]
        solver_var_related_input_array = [solver_var_related_inputs]
        solver_var_distinct_output_array = [solver_var_distinct_outputs]
        encoded_obligation1_array = [None]
        encoded_obligation2_array = [None]
        encoded_fp_array = [encoded_all_fp]

        same_1_array = [None]
        same_2_array = [None]
        neighbor1_array = [None]
        neighbor2_array = [None]

        encoded_loop_array = [False]

        for k in range(1, dmax+1):
            # copy variables
            copied_related_inputs, rename_map = self._copy_related_var_and_update_var_map(related_inputs=related_inputs, copied_time=k)
            copied_distinct_outputs, rename_map_do = self._copy_related_var_and_update_var_map(related_inputs=inde_outputs, copied_time=k)
            copied_ri_map = {v.id: solver.get_fresh_variable(v.id, sort=v.type_str) for v in copied_related_inputs}
            copied_do_map = {v.id: solver.get_fresh_variable(v.id, sort=v.type_str) for v in copied_distinct_outputs}
            vars_map.update(copied_ri_map)
            vars_map.update(copied_do_map)
            rename_map.update(rename_map_do)

            solver_var_copied_related_inputs = [vars_map[v.id] for v in copied_related_inputs]
            solver_var_copied_distinct_outputs = [vars_map[v.id] for v in copied_distinct_outputs]
            related_input_array.append(copied_related_inputs)
            distinct_output_array.append(copied_distinct_outputs)
            solver_var_related_input_array.append(solver_var_copied_related_inputs)
            solver_var_distinct_output_array.append(solver_var_copied_distinct_outputs)
 
            # copy clauses
            # the all fixed points should eliminate distinct output
            copied_all_fixed_points = self._copy_clause_with_copied_var(all_fixed_points, rename_map, copied_related_inputs + list(system_inputs) + copied_distinct_outputs)
            copied_obligation1 = self._copy_clause_with_copied_var(other1.obligation, rename_map, related_inputs + copied_related_inputs + list(system_inputs) + copied_distinct_outputs)
            copied_obligation2 = self._copy_clause_with_copied_var(other2.obligation, rename_map, related_inputs + copied_related_inputs + list(system_inputs) + copied_distinct_outputs)
            
            vars_map, encoded_all_fp_copied = copied_all_fixed_points.encode(solver=solver, vars=copied_all_fixed_points.vars, clause=copied_all_fixed_points.expr, vars_map=vars_map)
            vars_map, encoded_copied_obligation1 = copied_obligation1.encode(solver=solver, vars=copied_obligation1.vars, clause=copied_obligation1.expr, vars_map=vars_map)
            vars_map, encoded_copied_obligation2 = copied_obligation2.encode(solver=solver, vars=copied_obligation2.vars, clause=copied_obligation2.expr, vars_map=vars_map)

            # fixed encoded_all_fp_copied
            if solver_var_copied_distinct_outputs:
                encoded_all_fp_copied = solver.clause_exists(solver_var_copied_distinct_outputs, encoded_all_fp_copied)
            encoded_obligation1_array.append(encoded_copied_obligation1)
            encoded_obligation2_array.append(encoded_copied_obligation2)
            encoded_fp_array.append(encoded_all_fp_copied)

            # create equality constraints
            same_1, same_2 = self._generated_neighbor_constraint(solver=solver, 
                                                                related_inputs=related_inputs,
                                                                related_inputs_1=related_inputs_1,
                                                                related_inputs_2=related_inputs_2,
                                                                vars1=related_input_array[k-1],
                                                                vars2=related_input_array[k],
                                                                var_map=vars_map)
            same_1_array.append(same_1)
            same_2_array.append(same_2)

            # create loop constraints
            duplicate_constraint = []
            for i in range(k-1):
                same_1, same_2 = self._generated_neighbor_constraint(solver=solver, 
                                                                    related_inputs=related_inputs,
                                                                    related_inputs_1=related_inputs_1,
                                                                    related_inputs_2=related_inputs_2,
                                                                    vars1=related_input_array[i],
                                                                    vars2=related_input_array[k],
                                                                    var_map=vars_map)
                duplicate_constraint.append(solver.clause_and(same_1, same_2))
            if duplicate_constraint:
                encoded_loop = solver.clause_or(*duplicate_constraint)
                #print(encoded_loop)
                encoded_loop_array.append(encoded_loop)
            else:
                encoded_loop_array.append(False)

            # create neighbor constraints
            if solver_var_distinct_outputs:
                neighbor_clause_1 = solver.clause_and(same_1, solver.clause_exists(solver_var_distinct_outputs, encoded_copied_obligation1))
                neighbor_clause_2 = solver.clause_and(same_2, solver.clause_exists(solver_var_distinct_outputs, encoded_copied_obligation2))
            else:
                neighbor_clause_1 = solver.clause_and(same_1, encoded_copied_obligation1)
                neighbor_clause_2 = solver.clause_and(same_2, encoded_copied_obligation2)
            neighbor1_array.append(neighbor_clause_1)
            neighbor2_array.append(neighbor_clause_2)

        ret = None
        d = dinit
        while d < dmax:
            # positive proof
            LOG.debug(f"[INDE] Positive Proof [depth = {d}]")
            # create tree
            encoded_tree1_0 = solver.clause_forall(solver_var_related_input_array[d], solver.clause_implies(neighbor1_array[d], same_2_array[d]))
            encoded_tree2_0 = solver.clause_forall(solver_var_related_input_array[d], solver.clause_implies(neighbor2_array[d], same_1_array[d]))
            encoded_tree1_array = [encoded_tree1_0]
            encoded_tree2_array = [encoded_tree2_0]
            for k in range(1, d):
                print(k)
                encoded_tree1 = solver.clause_forall(solver_var_related_input_array[d-k], solver.clause_implies(neighbor1_array[d-k], solver.clause_or(encoded_tree2_array[k-1], same_2_array[d-k])))
                encoded_tree2 = solver.clause_forall(solver_var_related_input_array[d-k], solver.clause_implies(neighbor2_array[d-k], solver.clause_or(encoded_tree1_array[k-1], same_1_array[d-k])))
                encoded_tree1_array.append(encoded_tree1)
                encoded_tree2_array.append(encoded_tree2)

            encoded_positive_proof = solver.clause_and(encoded_assumption, solver.clause_forall(solver_var_related_input_array[0], 
                                                                                                solver.clause_or(solver.clause_not(encoded_fp_array[0]),
                                                                                                                 solver.clause_not(encoded_tree1_array[d-1]),
                                                                                                                 solver.clause_not(encoded_tree2_array[d-1]))

                                                                                                )
                                                    )

            solver.reset()
            solver.add_conjunction_clause(encoded_positive_proof)
            is_counter_env = solver.check()

            if is_counter_env:
                LOG.debug(f"[INDE] The environment {solver._model} does not possess a good fixed point group within {d} neighbors")
            else:
                LOG.debug(f"[INDE] Every targeted environment has a fixed point group smaller than depth {d}")
                ret = True
                break

            # negative proof
            LOG.debug(f"[INDE] Negative Proof [depth = {d}]")

            encoded_fail1 = solver.clause_exists(solver_var_related_input_array[d], solver.clause_and(neighbor1_array[d], solver.clause_not(encoded_fp_array[d])))
            encoded_fail2 = solver.clause_exists(solver_var_related_input_array[d], solver.clause_and(neighbor2_array[d], solver.clause_not(encoded_fp_array[d])))
            encoded_fail1_array = [encoded_fail1]
            encoded_fail2_array = [encoded_fail2]

            for k in range(1, d):
                encoded_fail1 = solver.clause_exists(solver_var_related_input_array[d-k], solver.clause_and(neighbor1_array[d-k], 
                                                                                                            solver.clause_not(same_2_array[d-k]),
                                                                                                            solver.clause_or(solver.clause_not(encoded_fp_array[d-k]),
                                                                                                                              encoded_fail2_array[k-1],
                                                                                                                              encoded_loop_array[d-k])))
                encoded_fail2 = solver.clause_exists(solver_var_related_input_array[d-k], solver.clause_and(neighbor2_array[d-k], 
                                                                                                            solver.clause_not(same_1_array[d-k]),
                                                                                                            solver.clause_or(solver.clause_not(encoded_fp_array[d-k]),
                                                                                                                              encoded_fail1_array[k-1],
                                                                                                                              encoded_loop_array[d-k])))
                encoded_fail1_array.append(encoded_fail1)
                encoded_fail2_array.append(encoded_fail2)

            encoded_negative_proof = solver.clause_and(encoded_assumption,  solver.clause_forall(solver_var_related_input_array[0],
                                                                                                solver.clause_implies(encoded_fp_array[0],
                                                                                                                        solver.clause_or(encoded_fail1_array[d-1],
                                                                                                                                         encoded_fail2_array[d-1]))))
            
            solver.reset()
            solver.add_conjunction_clause(encoded_negative_proof)
            is_counter_env = solver.check()
            if is_counter_env:
                LOG.debug(f"[INDE] The environment {solver._model} has all fixed point groups violating the condition within depth {d}")
                ret = False
                break
            else:
                LOG.debug(f"[INDE {d}] Not finding negative example within depth {d}... keep searching...")
            # increment
            d = d + 1
        return ret


    
    def _generated_neighbor_constraint(self, solver, related_inputs, related_inputs_1, related_inputs_2, vars1, vars2, var_map):
        same_1 = None
        same_2 = None
        for v1, v2, v3 in zip(related_inputs, vars1, vars2):
            eq_clause = var_map[v2.id] == var_map[v3.id]
            if v1 in related_inputs_1:
                if same_1 is not None:
                    same_1 = solver.clause_and(same_1, eq_clause)
                else:
                    same_1 = eq_clause
            elif v1 in related_inputs_2:
                if same_2 is not None:
                    same_2 = solver.clause_and(same_2, eq_clause)
                else:
                    same_2 = eq_clause   

        return same_1, same_2

    def _copy_related_var_and_update_var_map(self, related_inputs, copied_time:int):
        copied_related_inputs = []
        # change their name to internal copy
        rename_map = dict()
        for v in related_inputs:
            new_v = copy.copy(v)
            new_v.id = f"__copy{copied_time}__" + v.id
            copied_related_inputs.append(new_v)
            rename_map[v.id] = new_v.id
        return copied_related_inputs, rename_map

    def _copy_clause_with_copied_var(self, clause: FOLClauseSet, rename_map, copied_expr_var):
        copied_clause_expr = copy.deepcopy(clause.expr)
        name_remap(rename_map, copied_clause_expr.root)
        copied_clause_expr._symbols = copied_clause_expr.root.get_symbols()
        # create new fol clause set for it
        copied_clause = FOLClauseSet(vars = copied_expr_var, expr=copied_clause_expr)
        return copied_clause

    def _explored_fixed_point_explicit(self, other1: ContractBase, other2: ContractBase, explored_point, group: list, all_fixed_points, related_inputs, env_set, direction = None):
        LOG.debug(f"[INDE] Exploring {explored_point}")

        next_points1 = set()
        next_points2 = set()
        is_dirty1 = False
        is_dirty2 = False
        if direction == 1 or direction is None:
            neighbor_behaviors_1 = self._get_neighbors_explicit(explored_point, other1, related_inputs=related_inputs, env_set=env_set)
            LOG.debug(f"[INDE] Possible behaviors for C1 {neighbor_behaviors_1}")
            next_points1, is_dirty1 = self._check_neighbors_explicit(neighbors=neighbor_behaviors_1, explored_point=explored_point, group=group, all_fixed_points=all_fixed_points)
        if direction == 2 or direction is None:
            neighbor_behaviors_2 = self._get_neighbors_explicit(explored_point, other2, related_inputs=related_inputs, env_set=env_set)
            LOG.debug(f"[INDE] Possible behaviors for C2 {neighbor_behaviors_2}")
            next_points2, is_dirty2 = self._check_neighbors_explicit(neighbors=neighbor_behaviors_2, explored_point=explored_point, group=group, all_fixed_points=all_fixed_points)

        is_dirty = is_dirty1 or is_dirty2

        for next_point in next_points1:
            is_dirty |= self._explored_fixed_point_explicit(other1=other1, other2=other2, explored_point=next_point, group=group, all_fixed_points=all_fixed_points, related_inputs=related_inputs, env_set=env_set, direction=2)
        for next_point in next_points2:
            is_dirty |= self._explored_fixed_point_explicit(other1=other1, other2=other2, explored_point=next_point, group=group, all_fixed_points=all_fixed_points, related_inputs=related_inputs, env_set=env_set, direction=1)
        return is_dirty

    def _get_neighbors_explicit(self, fixed_point, other: ContractBase, related_inputs, env_set):
        ef_set = ExplicitSet(related_inputs, expr=[fixed_point])
        # get related inputs of the other
        related_input_other = set(other.assumption.ordered_vars).intersection(set(related_inputs))
        # #TODO: Debug this, the environment is not completely removed from this
        # print([v.id for v in related_input_other])
        neighbor_behaviors = ef_set.project(list(related_input_other), is_refine=False).intersect(env_set).intersect(other.guarantee)
        neighbor_behaviors = neighbor_behaviors.project(related_inputs)
        LOG.debug(f"[INDE] Possible behaviors {neighbor_behaviors}")
        #LOG.debug(f"[INDE] Possible behaviors {neighbor_behaviors}")
        return neighbor_behaviors.internal_expr



    def _check_neighbors_explicit(self, neighbors, explored_point, group, all_fixed_points):
        next_points = []
        dirty_flag = False
        for elem in neighbors:
            LOG.debug(f"[INDE] Checking Neighbor {elem}")
            if elem != explored_point:
                if elem in group:
                    # loop found
                    dirty_flag = True
                    LOG.debug(f"[INDE] Loop Found ({elem} already explored), the group is under the risk of dissappearing after refinement")
                else:
                    if elem not in all_fixed_points:
                        dirty_flag = True
                        LOG.debug(f"[INDE] Found non fixed point {elem} as neighbor, the group is under the risk of dissappearing after refinement")
                    else:
                        group.append(elem)
                        next_points.append(elem)
                LOG.debug(f"[INDE] Next Collect: {next_points} Group: {group}, Dirty: {dirty_flag}")
        return next_points, dirty_flag
    def to_cb(self):
        from contractda.contracts._cbcontract import CBContract
        return CBContract(vars=self._vars, constraint=self.environment, behavior=self.implementation)
