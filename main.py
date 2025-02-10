import random as r

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

class Grammar:
    def __init__(self, vn, vt, p):
        self.vn = vn
        self.vt = vt
        self.p = p

    def generate_string(self):
        string = ['S']

        while any(letter in self.vn for letter in string):
            steps = 0
            for letter in string:
                initial_step = f"{''.join(string)}"
                if letter in vn:
                    # select any appropriate rule
                    replacement = list(r.choice(P[letter]))
                    letter_index = string.index(letter)
                    string.pop(letter_index)

                    # derive replacement
                    for item in replacement:
                        string.insert(letter_index, item)
                        letter_index += 1
                steps += 1
                print(f"Step {steps}: {initial_step} → {''.join(string)}")

            print(f"Final word: {''.join(string)}")


# main
vn = ['S', 'A', 'B']
vt = ['a', 'b', 'c', 'd']

P = {
    'S': ['bS', 'dA'],
    'A': ['aA', 'dB', 'b'],
    'B': ['cB', 'a']
}

g1 = Grammar(vn, vt, P)
g1.generate_string()