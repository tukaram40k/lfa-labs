import re
import random as r

class Reg:
    def __init__(self, src):
        self.src = src
        
    # split re into tokens
    def scan_re(self):
        self.reg = [re.split(' ', i) for i in self.src]
        print(self.reg)
    
    def generate_str(self, n):
        strings = []
        
        # go through tokens
        for reg in self.reg:
            str = []
            
            for token in reg:
                result = []
                
                # check for *,+,?
                last = token[-1]
                if last == ')':
                    last = '1'
                    chars = (token + '.')[:-1]
                elif last in ['*', '+', '?']: chars = token[:-1]
                else: chars = (token + '.')[:-1]
                
                if last.isalpha(): last = '1'
                if ')' in chars and last.isdigit(): chars = chars[:-1]
                if '(' not in chars and ')' not in chars: last = '1'
                               
                # check for |
                chars = chars.replace('(', '')
                chars = chars.replace(')', '')
                chars = chars.split('|')
                
                print(f'token: {token:10} chars: {chars}, last: {last}')
                
                if last.isdigit():
                    ch = r.choice(chars)
                    for _ in range(int(last)):
                        result.append(ch)
                elif last == '?':
                    for _ in range(r.randint(0, 1)):
                        result.append(r.choice(chars))
                elif last == '+':
                    ch = r.choice(chars)
                    for _ in range(r.randint(1, 5)):
                        result.append(ch)
                elif last == '*':
                    ch = r.choice(chars)
                    for _ in range(r.randint(0, 5)):
                        result.append(ch)
                
                result = ''.join(result)
                str.append(result)
            
            strings.append(str)
        
        print(strings)
                
    
reg1 = Reg(['(a|b) (c|d) E+ G?', 'P (Q|R|S) T (UV|W|X)* Z+', '1 (0|1)* 2 (3|4)5 36'])
reg1.scan_re()
reg1.generate_str(1)