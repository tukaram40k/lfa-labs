from to_cnf import ToCNF

# var 25

vn = ['S', 'A', 'B', 'C', 'D']
vt = ['a', 'b']
p = {
    'S': ['bA', 'BC'],
    'A': ['a', 'aS', 'bCaCa'],
    'B': ['A', 'bS', 'bCAa'],
    'C': ['epsilon', 'AB'],
    'D': ['AB']
}
s = 'S'

g1 = ToCNF(vn, vt, p, s)
