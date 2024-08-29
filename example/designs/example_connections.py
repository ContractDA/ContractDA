from contractda.design._connections import Connection, Port
from contractda.design._port import VarType, PortDirection

if __name__ == "__main__":
    port1 = Port(port_name="testport1", port_type=VarType.REAL, direction=PortDirection.INOUT)
    port2 = Port(port_name="testport2", port_type=VarType.REAL, direction=PortDirection.INOUT)
    conn = Connection(name="net1", terminals=[port1, port2])
    conn.report()
    for terminal in conn.terminals:
        terminal.report()