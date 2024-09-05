from contractda.design._system import System
from contractda.design._libsystem import LibSystem
from contractda.design._connections import Connection, Port
from contractda.design._port import VarType, PortDirection
from contractda.design._system_contracts import SystemContract

if __name__ == "__main__":
    p_1a = Port(port_name="a", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_1b = Port(port_name="b", port_type=VarType.REAL, direction=PortDirection.OUTPUT)
    p_2a = Port(port_name="a", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_2b = Port(port_name="b", port_type=VarType.REAL, direction=PortDirection.OUTPUT)
    p_3a = Port(port_name="a", port_type=VarType.REAL, direction=PortDirection.INPUT)
    p_3b = Port(port_name="b", port_type=VarType.REAL, direction=PortDirection.OUTPUT)

    json_obj1 = {
        "name": "C1",
        "type": "AG",
        "content": {
            "assumption": {
                "set_type": "FOL",
                "description": "a >= 0"
            },
            "guarantee": {
                "set_type": "FOL",
                "description": "b == 2*a"
            }
        }
    }

    json_obj2 = {
        "name": "C2",
        "type": "AG",
        "content": {
            "assumption": {
                "set_type": "FOL",
                "description": "a >= 0"
            },
            "guarantee": {
                "set_type": "FOL",
                "description": "b == 4*a"
            }
        }
    }

    json_obj3 = {
        "name": "C3",
        "type": "AG",
        "content": {
            "assumption": {
                "set_type": "FOL",
                "description": "a >= 0"
            },
            "guarantee": {
                "set_type": "FOL",
                "description": "b == 8*a"
            }
        }
    }

    libsys1 = LibSystem(name="lib_test1", ports=[p_1a, p_1b], contracts=[SystemContract.from_dict(json_obj1)])
    libsys2 = LibSystem(name="lib_test2", ports=[p_2a, p_2b], contracts=[SystemContract.from_dict(json_obj2)])
    libsys3 = LibSystem(name="lib_test3", ports=[p_3a, p_3b], contracts=[SystemContract.from_dict(json_obj3)])

    libsys1.report()
    print(libsys1.to_dict())
    libsys2.report()
    print(libsys2.to_dict())
    libsys3.report()
    print(libsys3.to_dict())

    libsys4 = LibSystem.from_dict(libsys1.to_dict())
    libsys4.report()
    print(libsys4.to_dict())