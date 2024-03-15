from contractda.contracts._contract_base import ContractBase

if __name__ == "__main__":
    a = ContractBase()
    b = ContractBase()
    a.compose(b)
    ContractBase.compose(a, b)