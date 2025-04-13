import string

class ToCNF:
    def __init__(self, vn, vt, p, s):
        self.vn = vn
        self.vt = vt
        self.p = p
        self.s = s
        self.free_chars = list(string.ascii_uppercase)
        
        new_chars = []
        for ch in self.free_chars:
            if ch not in vn:
                new_chars.append(ch)
        
        self.free_chars = new_chars
        
    def next_free_ch(self):
        ch = self.free_chars.pop(0)
        return ch
    
    def __str__(self):
        return f'vn = {self.vn}; vt = {self.vt}; s = {self.s}\np = {self.p}\n'
        
    def rm_st_symbol(self):
        for vn, rules in self.p.items():
            for rule in rules:
                if self.s in rule:
                    new_s = self.next_free_ch()
                    self.p[new_s] = [self.s]
                    self.s = new_s
                    self.vn.append(new_s)
                    return
                    
    def rm_eprod(self):
        nullable = set()

        # find nullable vns
        changed = True
        while changed:
            changed = False
            for A in self.p:
                if A not in nullable:
                    for rule in self.p[A]:
                        if rule == 'epsilon' or all(symbol in nullable for symbol in rule):
                            nullable.add(A)
                            changed = True
                            break

        # remove e prod
        for A in list(self.p):
            self.p[A] = [rule for rule in self.p[A] if rule != 'epsilon']

        # add new prods
        for A in list(self.p):
            new_rules = set(self.p[A])
            
            for rule in self.p[A]:
                positions = [i for i, symbol in enumerate(rule) if symbol in nullable]
                n = len(positions)
                
                for i in range(1, 1 << n):
                    rule_list = list(rule)
                    for j in range(n):
                        if (i >> j) & 1:
                            rule_list[positions[j]] = ''
                    new_rule = ''.join(rule_list)
                    if new_rule != '':
                        new_rules.add(new_rule)
                    else:
                        new_rules.add('epsilon')
                        
            self.p[A] = list(new_rules)

        # check start symbol
        if self.s in nullable:
            if 'epsilon' not in self.p[self.s]:
                self.p[self.s].append('epsilon')
    
    def rm_uprod(self):
        # find unit prods
        unit_pairs = {vn: set() for vn in self.vn}

        for A in self.vn:
            for rule in self.p[A]:
                if len(rule) == 1 and rule in self.vn:
                    unit_pairs[A].add(rule)

        changed = True
        while changed:
            changed = False
            for A in self.vn:
                new_units = set()
                for B in unit_pairs[A]:
                    for C in unit_pairs.get(B, []):
                        if C not in unit_pairs[A]:
                            new_units.add(C)
                            changed = True
                unit_pairs[A].update(new_units)

        # add non-unit prods
        new_p = {}
        for A in self.vn:
            new_rules = [rule for rule in self.p[A] if not (len(rule) == 1 and rule in self.vn)]
            for B in unit_pairs[A]:
                for rule in self.p[B]:
                    if not (len(rule) == 1 and rule in self.vn):
                        new_rules.append(rule)
            new_p[A] = list(set(new_rules))  # remove dupes

        self.p = new_p

                
    
    def rm_extra_vars(self):
        pass
    
    def rm_extra_terms(self):
        pass