from contractda.contracts._contract_base import ContractBase
from contractda.contracts._agcontract import AGContract
from contractda.contracts._cbcontract import CBContract

class ContractOperation():
    """A class for static method on contract, all operation generate a new contract after the operation"""

    def __init__():
        pass

    @staticmethod
    def compose(c1: ContractBase, c2: ContractBase) -> ContractBase:
        pass

    @staticmethod
    def quotient(c1: ContractBase, c2: ContractBase) -> ContractBase:
        pass

    @staticmethod
    def merge(c1: ContractBase, c2: ContractBase) -> ContractBase:
        pass

    @staticmethod
    def separate(c1: ContractBase, c2: ContractBase) -> ContractBase:
        pass
    
    @staticmethod
    def conjunction(c1: ContractBase, c2: ContractBase) -> ContractBase:
        pass

    @staticmethod
    def implication(c1: ContractBase, c2: ContractBase) -> ContractBase:
        pass

    @staticmethod
    def convert_to_cb(c1: ContractBase) -> CBContract:
        """Convert any contract to CB Contract"""
        if isinstance(c1, AGContract):
            return CBContract(vars=c1.vs, constraint=c1.environment, behavior=c1.implementation)
        elif isinstance(c1, CBContract):
            return CBContract(vars=c1.vs, constraint=c1.environment, behavior=c1.implementation)
        else:
            raise Exception(f"Unable to convert type {type(c1)} to CB Contract")

    @staticmethod
    def convert_to_ag(c1: ContractBase) -> AGContract:
        """Convert any contract to CB Contract"""
        if isinstance(c1, CBContract):
            return AGContract(vars=c1.vs, constraint=c1.environment, behavior=c1.implementation)
        if isinstance(c1, AGContract):
            return AGContract(vars=c1.vs, constraint=c1.environment, behavior=c1.implementation)
        else:
            raise Exception(f"Unable to convert type {type(c1)} to AG Contract")