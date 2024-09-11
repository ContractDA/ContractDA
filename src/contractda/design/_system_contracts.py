
from enum import Enum
from jsonschema import validate, ValidationError
from contractda.logger._logger import LOG

class ContractType(Enum):
    """Enum for contract type
    """
    AG = 0,
    CB = 1

class SetType(Enum):
    """Enum for Set type"""
    FOL = 0,
    LTL = 1,
    EXPLICIT_SET = 2,
    
class SystemContract():
    """A wrapper for storing contract description and the actual contract object
    """
    def __init__(self, name:str, type:ContractType):
        self._contract_obj = None
        self._type = type
        self._name = name
        self._description = None
        pass

    def __str__(self) -> str:
        description = ", ".join([f"{set_name}: {set_content['description']}" for set_name, set_content in self._description.items()])
        return f"{self._type.name}Contract {self._name}: {description}"
        
    @property
    def name(self) -> str:
        return self._name
    @property
    def type(self) -> ContractType:
        return self._type

    set_schema = {
        "type": "object",
        "properties": {
            "set_type": {"type": "string"},
            "description": {"type": "string"}
        }
    }

    ag_contract_schema = {
        "type": "object",
        "properties":{
            "assumption": set_schema,
            "guarantee": set_schema
        }
    }

    cb_contract_schema = {
        "type": "object",
        "properties":{
            "assumption": set_schema,
            "guarantee": set_schema
        }
    }

    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "type": {"type": "string"},
            "content": {"type": "object"}
        },
        "required": ["name", "type", "content"]
    }

    def to_dict(self) -> dict:
        return {
            "name": self._name,
            "type": self._type.name,
            "content": self._description
        }

    @classmethod
    def from_dict(cls, dict_obj):
        try:
            validate(instance=dict_obj, schema=cls.schema)
        except ValidationError as e:
            LOG.error(f"Contract Definition Error {repr(e)}")
            return None
        
        new_inst = cls(name=dict_obj["name"], type=ContractType[dict_obj["type"]])
        new_inst._description = dict_obj["content"]
        return new_inst

