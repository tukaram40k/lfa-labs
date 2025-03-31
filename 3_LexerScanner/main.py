from lexer import Lexer

path = f'./3_LexerScanner/eg1.txt'
# path = f'./3_LexerScanner/eg2.txt'

with open(path, 'r') as file:
    text = file.read()
    
    l1 = Lexer(text)
    l1.tokenize()
    l1.print_tokens()