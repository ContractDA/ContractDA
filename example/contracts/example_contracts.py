

if __name__ == "__main__":
    # define sybmol type

    # set level

    #
    x = RealVar("x")
    y = RealVar("y")
    z = RealVar("z")
    c1 = Contracts(domain = {x, y}, parameter = {}, contract_type = "ag", assumption = "x > 5", guarantee = "y = 2*x") # add parameter to denote a set of contracts
    c2 = Contracts(domain = {y, z}, contract_type = "ag", assumption = "y = ", guarantee = "(y == x) && (z == x*2)")
    c3 = Contracts(domain = {y, z}, contract_type = "ag", assumption = "y = ", guarantee = "(y == x) && (z == x*4)")
    # contract level api
    # in contract level, we assume the designer take care of the variables, i.e. we don't care about the system and connection
    # this level handles the contract operation, independent design, 
    # allow us to define whether it is a ag contract or cb contract, perform operation, and check refienment, independent design, consistency, compatipability

    c1.is_refine(c2) ### true
    c1.is_receptive() ### true
    c1.check_ind_decomp(c2, c3) # check if the decomposition follows independent design
    c4 = c1.compose(c2)


    # system level: perform component selection and simulation
    
    sys = System(name="Top", ports = {x, y, z}, obj = Objective(condition = "x = 4", obj = "x+z"), spec = c3, spec_ports_map = {},)

    # contract simulation
    sys.simulate(condition = "x < 3", observe_val = "x+y")

    # contract system verification 
    sys.add_subsystem(sys2) # subsystem (which might also be constructed by internal subsystem) # single subsystem means single refinement
    sys.add_subsystem(sys2, sys3, connection={}) # subsystem decomposition..

    #component selection (applied when there exist different contract)
    # parameter-based selection 
    # different contract selection
    sys2.add_selection([]) # list of contract or list of parametrized contract with the set of parameter -> clauseSet or explicit set
    # define a type of component, which follows a certain contract 
    sys.select()
    # Contract Manager, help with scope of different contracts and system
    mgr = Contract_Manager() # consider a design
    component_1 = Component()
    Ports = {x, y, z}
    sys1 = System(ports = {x, y, z}, contracts = c1, param = ) # get instance of sys1
    sys2 = System(ports = {x, y, z}, contracts = c1)
    mgr.