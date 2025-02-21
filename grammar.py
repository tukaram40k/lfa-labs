import random as r

class Grammar:
    def __init__(self, vn, vt, p):
        self.vn = vn
        self.vt = vt
        self.p = p

    # this generates a random string according to the rules
    def generate_string(self, print_steps=False):
        string = ['S']

        while any(letter in self.vn for letter in string):
            steps = 0
            for letter in string:
                initial_step = f"{''.join(string)}"
                if letter in self.vn:
                    # select any appropriate rule
                    replacement = list(r.choice(self.p[letter]))
                    letter_index = string.index(letter)
                    string.pop(letter_index)

                    # derive replacement
                    for item in replacement:
                        string.insert(letter_index, item)
                        letter_index += 1

                steps += 1
                if print_steps: print(f"Step {steps}: {initial_step} → {''.join(string)}")

            if print_steps: print(f"Final word: {''.join(string)}")

            return ''.join(string)

    # this returns n unique strings
    def get_n_strings(self, n):
        words = []
        while len(words) < n:
            word = self.generate_string()
            if word not in words: words.append(word)

        return words