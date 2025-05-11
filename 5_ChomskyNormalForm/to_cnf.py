import string

class ToCNF:
    def __init__(self, vn, vt, p, s):
        self.vn = vn
        self.vt = vt
        self.p = p
        self.s = s
        
        en_ch = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
        ru_ch = [chr(i) for i in range(ord('А'), ord('Я') + 1)]
        for ch in ['А', 'В', 'С', 'Е', 'К', 'Н', 'Р', 'О', 'Т', 'М', 'У', 'Х']:
            if ch in ru_ch:
                ru_ch.remove(ch)
        cn_ch = [chr(i) for i in range(int('0x4E00', 16) + 500, int('0x9FFF', 16) + 1)]
        self.free_chars = en_ch + ru_ch + cn_ch
        
        new_chars = []
        for ch in self.free_chars:
            if ch not in vn:
                new_chars.append(ch)
        
        self.free_chars = new_chars
        
    def next_free_ch(self):
        ch = self.free_chars.pop(0)
        return ch
    
    def __str__(self):
        return f'Vn = {self.vn}\n\nVt = {self.vt}\nS = {self.s}\n\nP = {self.p}\n'
        
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
    
    def rm_useless(self):
        reachable = set()
        reachable.add(self.s)
        
        to_process = [self.s]
        
        while to_process:
            current = to_process.pop()
            if current in self.p:
                for rule in self.p[current]:
                    for symbol in rule:
                        if symbol in self.vn and symbol not in reachable:
                            reachable.add(symbol)
                            to_process.append(symbol)
        
        unreachable_vn = set(self.vn) - reachable
        self.vn = [vn for vn in self.vn if vn not in unreachable_vn]
        
        for vn in unreachable_vn:
            if vn in self.p:
                del self.p[vn]
        
        used_terminals = set()
        for rules in self.p.values():
            for rule in rules:
                for symbol in rule:
                    if symbol in self.vt:
                        used_terminals.add(symbol)
        
        self.vt = [vt for vt in self.vt if vt in used_terminals]
    
    def rm_extra_vars(self):
        # Create a copy of the productions to avoid modification during iteration
        productions = list(self.p.items())
        for A, rules in productions:
            new_rules = []
            for rule in rules:
                if len(rule) <= 2:
                    new_rules.append(rule)
                else:
                    symbols = list(rule)
                    num_new_vars = len(symbols) - 2
                    new_vars = [self.next_free_ch() for _ in range(num_new_vars)]
                    for var in new_vars:
                        self.vn.append(var)
                    # Add the first new rule: A -> symbols[0] new_vars[0]
                    new_rule_part = symbols[0] + new_vars[0]
                    new_rules.append(new_rule_part)
                    # Add productions for the new variables
                    for i in range(num_new_vars):
                        current_var = new_vars[i]
                        if i == num_new_vars - 1:
                            rhs = symbols[i+1] + symbols[i+2]
                        else:
                            rhs = symbols[i+1] + new_vars[i+1]
                        if current_var not in self.p:
                            self.p[current_var] = []
                        self.p[current_var].append(rhs)
            # Update A's productions, removing duplicates
            self.p[A] = list(set(new_rules))

    def rm_extra_terms(self):
        term_to_var = {}
        # Create new variables for each terminal
        for terminal in self.vt:
            if terminal not in term_to_var:
                new_var = self.next_free_ch()
                term_to_var[terminal] = new_var
                self.vn.append(new_var)
                self.p[new_var] = [terminal]
        # Replace terminals in the rules
        for A in list(self.p.keys()):
            new_rules = []
            for rule in self.p[A]:
                if len(rule) == 1 and rule in self.vt:
                    # Keep single terminals as they are
                    new_rules.append(rule)
                else:
                    # Replace each terminal with its corresponding variable
                    new_rule = []
                    for symbol in rule:
                        if symbol in term_to_var:
                            new_rule.append(term_to_var[symbol])
                        else:
                            new_rule.append(symbol)
                    new_rule = ''.join(new_rule)
                    new_rules.append(new_rule)
            # Update the productions, removing duplicates
            self.p[A] = list(set(new_rules))
            
    def convert(self):
        self.rm_st_symbol()
        print("=========== removed starting symbol from production rules ===========\n", self)
        self.rm_eprod()
        print("=========== removed null productions ===========\n", self)
        self.rm_uprod()
        print("=========== removed unit productions ===========\n", self)
        self.rm_useless()
        print("=========== removed unreachable symbols ===========\n", self)
        self.rm_extra_vars()
        self.rm_extra_terms()
        print("=========== turned remaining rules into cnf ===========\n", self)