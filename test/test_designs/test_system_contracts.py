import pytest
from contractda.design import SystemContract, ContractType

@pytest.fixture
def example_dict():
    json_obj = {
        "name": "C1",
        "type": "AG",
        "content": {
            "assumption": {
                "set_type": "FOL",
                "description": "a >= 0"
            },
            "guarantee": {
                "set_type": "FOL",
                "description": "y = a+b"
            }
        }
    }

    json_obj2 = {
        "name": "C2",
        "type": "CB",
        "content": {
            "constraint": {
                "set_type": "FOL",
                "description": "IV<= 100"
            },
            "behavior": {
                "set_type": "FOL",
                "description": "V=I*5"
            }
        }
    }
    return [json_obj, json_obj2]

@pytest.fixture
def example_system_contracts(example_dict):
    return [SystemContract.from_dict(json_obj) for json_obj in example_dict]


def test_name(example_system_contracts):
    assert(example_system_contracts[0].name == "C1")
    assert(example_system_contracts[1].name == "C2")

def test_type(example_system_contracts):
    assert(example_system_contracts[0].type == ContractType.AG)
    assert(example_system_contracts[1].type == ContractType.CB)

def test_str(example_system_contracts):
    str(example_system_contracts[0])
    str(example_system_contracts[1])

def test_to_dict(example_system_contracts, example_dict):
    for contract, dict_obj in zip(example_system_contracts, example_dict):
        contract_dict = contract.to_dict()
        assert(contract_dict["name"] == dict_obj["name"])
        assert(contract_dict["type"] == dict_obj["type"])

def test_wrong_dict_obj():
    json_obj = {
        "name": "C1",
        "content": {
            "assumption": {
                "set_type": "FOL",
                "description": "a >= 0"
            },
            "guarantee": {
                "set_type": "FOL",
                "description": "y = a+b"
            }
        }
    }
    assert(SystemContract.from_dict(json_obj) is None)