from contractda.contracts._contract_base import ContractBase

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

