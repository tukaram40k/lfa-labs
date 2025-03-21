from enum import Enum

class TokenType(Enum):
    faction = 'FACTION'
    str = 'HIGH GOTHIC SPEECH'
    deploy = 'DEPLOY'
    identifyer = 'BRAVE WARRIORS'
    equals = 'BY GOD EMPEROR\'S DECREE'
    num = 'NUMBER'
    cast = 'CAST'
    vox = 'VOX TRANSMISSION'
    engage = 'FOR THE EMPEROR!'
    lpar = 'IMPERIAL DECREE START'
    rpar = 'IMPERIAL DECREE END'
    
class Token:
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        self.pos = pos
        
    def __str__(self):
        return f'type: {self.type}, position: {self.pos}, value: {self.value}'
        
class Lexer:
    def __init__(self, src):
        self.src = src
        self.pos = 0
        self.tokens = []
        
    def skip(self):
        self.pos += 1
        
    # handle " "
    def take_str(self):
        self.skip()
        start = self.pos
        while (self.pos < len(self.src) and self.src[self.pos] != '"'):
            self.skip()
        val = self.src[start:self.pos]
        self.skip()
        return Token(str, val, start)
        
        
    def tokenize(self):
        def isspace(char):
            return (char == ' ')
            
        while(self.pos < len(self.src)):
            current = self.src[self.pos]
            
            if isspace(current): self.skip()
            elif 
                