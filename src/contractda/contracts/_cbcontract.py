from contractda.contracts._contract_base import ContractBase
from contractda.sets import SetBase, FOLClauseSet
from contractda.vars import Var

class CBContract(ContractBase):
    """Class for Constraint-Behavior Contract (CB Contract)

    A constraint-behavior contract defines the contract by constraint and intrinsic behavior.
    The intrinsic behavior is the e responsibility of the component, typically expressed in physical quantities.
    Constraints define the conditions under which the behaviors apply.
    """

    def __init__(self, vars: list[Var], constraint: SetBase | str, behavior: SetBase | str, language = "FOL"):
        """Constructor

        :param list[Var] vars: the variables
        :param constraint SetBase|str: the constraint
        :param constraint SetBase|str: the intrinsic behavior
        """
        self._constraint: SetBase = self._convert_to_sets_based_on_language(vars, constraint, language)
        self._intrinsic_behavior: SetBase = self._convert_to_sets_based_on_language(vars, constraint, language)

    def __str__(self):
        return f" CB Contract: Constraint: {self.constraint}, Behavior: {self.intrinsic_behavior}"
    @property
    def constraint(self) -> SetBase:
        """The constraint of the """
        return self._constraint
    
    @property
    def intrinsic_behavior(self) -> SetBase:
        return self._intrinsic_behavior
    
    def environment(self) -> SetBase:
        """ The targeted environment specified by the contracts"""
        pass
    
    def implementation(self) -> SetBase:
        """ The allowed implementation specified by the contracts"""
        pass

    ##################################
    #   Contract Property
    ##################################
    def is_receptive(self) -> bool:
        """ Whether the contract is recptive

        Receptive means for each targeted environment, there is a allowed behavior.
        :return: True if the contract is receptive, False if not
        :rtype: bool
        """
        pass

    def is_compatible(self) -> bool:
        """ Whether the contract is compatible

        A contract is compatible if the implementation set is not empty
        Receptive means for each targeted environment, there is a allowed behavior.
        :return: True if the contract is compatible, False if not
        :rtype: bool
        """
        pass

    def is_consistent(self) -> bool:
        """ Whether the contract is consistent

        A contract is consistent if the environment set is not empty
        :return: True if the contract is consistent, False if not
        :rtype: bool
        """
        pass
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
        if isinstance(other, self.__class__):
            # both CB contract, perform operation
            constr1 = self.constraint
            constr2 = other.constraint
            new_constr = constr1.intersect(constr2)

            behavior1 = self.intrinsic_behavior
            behavior2 = other.intrinsic_behavior
            new_behavior = behavior1.intersect(behavior2)

            self._constraint = new_constr
            self._intrinsic_behavior = new_behavior
            return self
        else:
            raise Exception("Not supported contract type")
    
    def quotient(self, other: ContractBase):
        """ Finding missing component contracts in the system

        Given system contract a, subsystem contract b, the quotient finds the contract c such that c compose b equals a
        This method will update the contract of itself inplace.

        :param ContractBase other: the known subsystem contract
        :return: the quotient result 
        :rtype: ContractBase
        """
        pass

    def conjunction(self, other: ContractBase):
        """ Combining different condition contracts

        Given system condition contract a and b, the conjunction finds the contract c such that c is satisfied if and only if either a or b is satisfied
        This method will update the contract of itself inplace.

        :param ContractBase other: the other contract to perform conjunction with this contract
        :return: the conjunction result
        :rtype: ContractBase
        """
        pass

    def implication(self, other: ContractBase):
        """ Finding the missing condition

        Given system contract a and know condition contract b, the implication finds the contract c such that the conjunction of b and c becomes a
        This method will update the contract of itself inplace.

        :param ContractBase other: the other contract to perform implication with this contract
        :return: the implication result
        :rtype: ContractBase
        """
        pass

    def merging(self, other: ContractBase):
        """ Combining different viewpoint contracts

        Given system viewpoint contract a and b, the mergin finds the contract c such that c is satisfied if and only if either a or b is satisfied
        This method will update the contract of itself inplace.

        :param ContractBase other: the other contract to perform conjunction with this contract
        :return: the merging result
        :rtype: ContractBase
        """
        pass


    def separation(self, other: ContractBase):
        """ Combining different viewpoint contracts

        Given system contract a and know viewpoint contract b, the implication finds the contract c such that the merging of b and c becomes a
        This method will update the contract of itself inplace.

        :param ContractBase other: the other contract to perform implication with this contract
        :return: the separation result
        :rtype: ContractBase
        """
        pass

    ##################################
    #   Contract Relations
    ##################################
    def is_refined_by(self, other: ContractBase) -> bool:
        """ Whether the contract is refined by the other contract

        Refinement means
        :param ContractBase others: all the subsystem contracts of :class:`~contract.contracts.ContractBase` 
        :return: True if the contract is refined by the others, False if not
        :rtype: bool
        """
        if isinstance(other, self.__class__):
            pass
            # both CB contract
        pass

    def is_strongly_replaceable_by(self, other: ContractBase) -> bool:
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
        pass

    def is_replaceable_by(self, other: ContractBase) -> bool:
        """ Check if the contract is replaceable by the other contract

        Contract A is replaceable by contract B if contract B has behavior under some targeted environment of A.

        Replaceability is an important property to ensure we can implementation a nonvacuous design of the original contract based on the refined contract.

        :param ContractBase other: the other contract to be checked if it replaces this contract
        :return: True if the contract is strongly replaceable by the other, False if not
        :rtype: bool
        """
        pass

    def is_independent_decomposition_of(self, other1: ContractBase, other2: ContractBase) -> bool:
        """ Check if the contract decomposition can allowed independent receptive refinement without causing vacuous design.

        TO BE ADDED (new contribution)
        :param ContractBase other1: one of the decomposition contract
        :param ContractBase other2: one of the decomposition contract
        :return: True if the contract is refined by other, False if not
        :rtype: bool
        """
        pass

