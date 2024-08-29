from contractda.design._system import System
from contractda.design._connections import Connection, Port
from contractda.design._port import VarType, PortDirection


if __name__ == "__main__":
    porta = Port(port_name="testport", port_type=VarType.REAL, direction=PortDirection.INOUT)
    porta.report()

    porta_json = porta.to_dict()
    print(porta.to_dict())
    portb = Port.from_dict(porta_json)
    portb.report()