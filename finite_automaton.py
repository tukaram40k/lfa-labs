class FiniteAutomaton:
    def __init__(self, vt, p):
        self.vt = vt
        self.p = p
        self.trans = self.map_transitions()

    def map_transitions(self):
        vt = self.vt
        p = self.p

        trans = {}

        for vn, rules in p.items():
            for rule in rules:
                if len(rule) == 1 and rule in vt:  # terminal leads to final state
                    trans[(vn, rule)] = 'final'
                elif len(rule) >= 2:
                    symbol = rule[0]
                    next = rule[1]
                    trans[(vn, symbol)] = next

        return trans

    def print_transitions(self):
        print(self.trans)

    def str_belongs_to_lang(self, str):
        q = 'S'
        for s in str:
            if (q, s) not in self.trans:
                return False
            q = self.trans[(q, s)]
        return q == 'final'