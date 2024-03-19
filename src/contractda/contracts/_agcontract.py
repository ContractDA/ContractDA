from contractda.contracts._contract_base import ContractBase
from contractda.sets import SetBase, FOLClauseSet, ExplicitSet
from contractda.vars import Var
from contractda.solvers import SolverInterface

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
        self._vars = vars

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
    def environment(self) -> SetBase:
        """ The targeted environment specified by the contracts"""
        return self.assumption
    
    @property
    def implementation(self) -> SetBase:
        """ The allowed implementation specified by the contracts"""
        return self.guarantee.union(self.assumption.complement())
    
    @property
    def assumption_vs(self) -> list[Var]:
        symbols = self.assumption.expr.get_symbols()
        return [v for v in self.vs if v.id in symbols]
    
    @property
    def non_assumption_vs(self) -> list[Var]:
        assumption_symbols = self.assumption.expr.get_symbols()
        return [v for v in self.vs if v.id not in assumption_symbols]        
    
    @property
    def obligation(self) -> SetBase:
        """ The contract obligation, see Beneviste et al. Multiple Viewpoint Contract-Based Specification and Design, FMCO07"""
        return self.guarantee.intersect(self.assumption)

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

        :param ContractBase others: all the subsystem contracts of :class:`~contract.contracts.ContractBase` 
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
            exist_vs = [var_map[v.id] for v in other.non_assumption_vs]
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
            raise NotImplementedError

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
        if solver is not None:
            raise NotImplementedError("I have not implement user specified solver for internal set operation")
        
        return self.assumption.intersect(other.guarantee).is_satifiable()

    def is_independent_decomposition_of(self, other1: ContractBase, other2: ContractBase) -> bool:
        """ Check if the contract decomposition can allowed independent receptive refinement without causing vacuous design.

        TO BE ADDED (new contribution)

        :param ContractBase other1: one of the decomposition contract
        :param ContractBase other2: one of the decomposition contract
        :return: True if the contract is refined by other, False if not
        :rtype: bool
        """
        pass

    def to_cb(self):
        from contractda.contracts._cbcontract import CBContract
        return CBContract(vars=self._vars, constraint=self.environment, behavior=self.implementation)
