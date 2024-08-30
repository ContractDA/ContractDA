from contractda.design._system import System, LibSystem
from contractda.design._system_contracts import SystemContract
from contractda.design._port import VarType, PortDirection
from contractda.contracts import AGContract
import json

if __name__ == "__main__":
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
    c1 = SystemContract.from_dict(json_obj)
    c2 = SystemContract.from_dict(json_obj2)
    print(c1.to_dict())
    print(c2.to_dict())
    c3 = SystemContract.from_dict(c1.to_dict())
    print(c1)
    print(c2)
    print(c3)
    print(c3.to_dict())