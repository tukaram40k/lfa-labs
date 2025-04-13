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
                
        if len(self.free_chars) != len(vn) + len(new_chars): print('свободные символы посчитал криво дурень')
        
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
        pass
    
    def rm_uprod(self):
        pass
    
    def rm_extra_vars(self):
        pass
    
    def rm_extra_terms(self):
        pass