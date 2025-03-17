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
    
    # classify grammar based on Chomsky hierarchy
    def classify(self):
        type3 = True
        type2 = True
        type1 = True
        
        for lhs, rhs_list in self.p.items():
            if lhs not in self.vn:
                return "type 0 unrestricted"
            
            for rhs in rhs_list:
                lhs_len = len(lhs)
                rhs_len = len(rhs)
                
                # check if all are context free
                if lhs_len != 1:
                    type2 = False
                
                # check if all are context sensitive
                if lhs_len > rhs_len:
                    type1 = False
                
                # check if all are regular
                if not ((rhs[0] in self.vt and (len(rhs) == 1 or (len(rhs) == 2 and rhs[1] in self.vn)))):
                    type3 = False
        
        if type3:
            return "type 3 regular"
        elif type2:
            return "type 2 context free"
        elif type1:
            return "type 1 context sensitive"
        else:
            return "type 0 unrestricted"