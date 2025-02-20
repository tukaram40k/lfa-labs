class FiniteAutomaton:
    def __init__(self, vn, vt, p):
        self.Q = vn # мб это не нужно
        self.vt = vt
        self.p = p
        self.transitions = self.map_transitions()

    def map_transitions(self):
        vt = self.vt
        p = self.p

        trans = {}

        for vn, rules in p.items():
            for rule in rules:
                if len(rule) == 1 and rule in vt:  # terminal leads to final state
                    trans[(vn, rule)] = 'FINAL'
                elif len(rule) >= 2:
                    symbol = rule[0]
                    next = rule[1]
                    trans[(vn, symbol)] = next

        return trans

    def print_transitions(self):
        print(self.transitions)

    def str_belongs_to_lang(self, str):
        pass