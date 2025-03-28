from contractda.contracts import CBContract, AGContract
from contractda.vars import Var, RealVar

x = RealVar("x")
y = RealVar("y")
z = RealVar("z")

c1 = AGContract(vars=[x, y, z], inputs=[x, z], assumption="true", guarantee="y == z + 1 || y == x * z")
c2 = AGContract(vars=[y, z], inputs=[y], assumption="true", guarantee="z == y + 1")
cs = AGContract(vars=[x, y], inputs=[x], assumption="x != 1", guarantee="y == x / (1 - x)")

print("Do c1 and c2 form a correct decomposition of cs?")
print(cs.is_independent_decomposition_of(c1, c2))

print("Do the composition of c1 and c2 refine cs?")
print(cs.is_refined_by(c1.composition(c2)))
    
