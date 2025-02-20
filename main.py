from grammar import Grammar
from finite_automaton import FiniteAutomaton

# Variant 25:
# VN={S, A, B},
# VT={a, b, c, d},
# P={
#     S → bS
#     S → dA
#     A → aA
#     A → dB
#     B → cB
#     A → b
#     B → a
# }

vn = ['S', 'A', 'B']
vt = ['a', 'b', 'c', 'd']

p = {
    'S': ['bS', 'dA'],
    'A': ['aA', 'dB', 'b'],
    'B': ['cB', 'a']
}

g1 = Grammar(vn, vt, p)
# print(g1.get_n_strings(10))

a1 = FiniteAutomaton(g1.vn, g1.vt, g1.p)
a1.map_transitions()
a1.print_transitions()
