from to_cnf import ToCNF

# var 25
vn = ['S', 'A', 'B', 'C', 'D']
vt = ['a', 'b']
p = {
    'S': ['bA', 'BC'],
    'A': ['a', 'aS', 'bCaCa'],
    'B': ['A', 'bS', 'bCA'],
    'C': ['epsilon', 'AB'],
    'D': ['AB']
}
s = 'S'

g1 = ToCNF(vn, vt, p, s)
g1.rm_st_symbol()
g1.rm_eprod()
g1.rm_uprod()
g1.rm_extra_vars()
g1.rm_extra_terms()

print(g1)
