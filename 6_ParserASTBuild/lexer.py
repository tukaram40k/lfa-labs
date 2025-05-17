from enum import Enum

class TokenType(Enum):
    faction = 'FACTION'
    str = 'HIGH GOTHIC SPEECH'
    deploy = 'DEPLOY'
    identifier = 'BRAVE WARRIORS'
    equals = 'BY GOD EMPEROR\'S DECREE'
    num = 'MEN AT ARMS'
    cast = 'CAST'
    vox = 'VOX TRANSMISSION'
    engage = 'FOR THE EMPEROR!'
    lpar = 'IMPERIAL DECREE START'
    rpar = 'IMPERIAL DECREE END'
    eof = 'END OF CRUSADE'
    invalid = 'TRAITOR'
    
class Token:
    def __init__(self, type, value, pos):
        self.type = type
        self.value = value
        self.pos = pos
        
    def __str__(self):
        return f"type: {self.type.value:25} value: {self.value}"

class Lexer:
    def __init__(self, src):
        self.src = src
        self.pos = 0
        self.tokens = []
        
    def skip(self):
        self.pos += 1
        
    def take_str(self):
        self.skip()  # Skip opening quote
        start = self.pos
        while self.pos < len(self.src) and self.src[self.pos] != '"':
            self.skip()
        if self.pos >= len(self.src):
            raise SyntaxError("Unterminated string literal")
        val = self.src[start:self.pos]
        self.skip()  # Skip closing quote
        return Token(TokenType.str, val, start)
        
    def take_keyword(self):
        start = self.pos
        while (self.pos < len(self.src)) and (self.src[self.pos].isalnum() or self.src[self.pos] == '_'):
            self.skip()
        val = self.src[start:self.pos]
        
        kws = {
            "faithful": TokenType.faction,
            "heretic": TokenType.faction,
            "deploy": TokenType.deploy,
            "engage": TokenType.engage,
            "cast": TokenType.cast,
            "vox_transmit": TokenType.vox
        }
        
        return Token(kws.get(val, TokenType.identifier), val, start)
    
    def take_num(self):
        start = self.pos
        while self.pos < len(self.src) and self.src[self.pos].isdigit():
            self.skip()
        val = self.src[start:self.pos]
        return Token(TokenType.num, val, start)
        
    def tokenize(self):
        while self.pos < len(self.src):
            char = self.src[self.pos]
            
            if char.isspace(): 
                self.skip()
            elif char.isdigit():
                self.tokens.append(self.take_num())
            elif char.isalpha() or char == '_':
                self.tokens.append(self.take_keyword())
            elif char == '"':
                self.tokens.append(self.take_str())
            elif char == '=':
                self.tokens.append(Token(TokenType.equals, '=', self.pos))
                self.skip()
            elif char == '{':
                self.tokens.append(Token(TokenType.lpar, '{', self.pos))
                self.skip()
            elif char == '}':
                self.tokens.append(Token(TokenType.rpar, '}', self.pos))
                self.skip()
            else:
                self.tokens.append(Token(TokenType.invalid, char, self.pos))
                self.skip()
                
        # Add EOF token at the end
        self.tokens.append(Token(TokenType.eof, "", self.pos))
        return self.tokens
                
    def print_tokens(self):
        for i, token in enumerate(self.tokens):
            print(f"token {i+1:3}   {token}")