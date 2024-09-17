
from enum import Enum
from jsonschema import validate, ValidationError
from contractda.logger._logger import LOG
from contractda.vars import Var
from contractda.contracts import AGContract, CBContract, ContractBase
from contractda.sets._fol_clause import FOLClause
from contractda.sets import FOLClauseSet

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
        self._contract_obj: ContractBase = None
        self._type: ContractType = type
        self._name: str = name
        self._description: dict = None
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
    
    def convert_to_contract_object(self, vars: list[Var], vars_remap: dict[str, str]) -> ContractBase:
        if self._type == ContractType.AG:
            language_a = self._description["assumption"]["set_type"]
            desc_a = self._description["assumption"]["description"]
            if language_a == "FOL":
                clause_instance_a = FOLClause(description=desc_a, ctx=None)
                clause_instance_a.rename_symbols(vars_remap=vars_remap)

            language_g = self._description["guarantee"]["set_type"]
            desc_g = self._description["guarantee"]["description"]
            if language_g == "FOL":
                clause_instance_g = FOLClause(description=desc_g, ctx=None)
                clause_instance_g.rename_symbols(vars_remap=vars_remap)

            assumption = FOLClauseSet(vars=vars, expr=clause_instance_a)
            guarantee = FOLClauseSet(vars=vars, expr=clause_instance_g)
            self._contract_obj = AGContract(vars=vars, assumption=assumption, guarantee=guarantee, language="FOL")
            return self._contract_obj
        elif self._type == ContractType.CB:
            language_c = self._description["constraint"]["set_type"]
            desc_c = self._description["constraint"]["description"]
            if language_c == "FOL":
                clause_instance_c = FOLClause(description=desc_c, ctx=None)
                clause_instance_c.rename_symbols(vars_remap=vars_remap)

            language_b = self._description["behavior"]["set_type"]
            desc_b = self._description["behavior"]["description"]
            if language_b == "FOL":
                clause_instance_b = FOLClause(description=desc_b, ctx=None)
                clause_instance_b.rename_symbols(vars_remap=vars_remap)

            constraint = FOLClauseSet(vars=vars, expr=clause_instance_c)
            behavior = FOLClauseSet(vars=vars, expr=clause_instance_b)
            self._contract_obj = CBContract(vars=vars, constraint=constraint, behavior=behavior, language="FOL")
            return self._contract_obj
        else:
            LOG.error(f"Not supported contract type {self._type}") 

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

