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
        
    def rm_st_symbol(self):
        pass
                    
    
    def rm_eprod(self):
        pass
    
    def rm_uprod(self):
        pass
    
    def rm_extra_vars(self):
        pass
    
    def rm_extra_terms(self):
        pass