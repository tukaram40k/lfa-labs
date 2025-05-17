from lexer import Lexer
from parser_40k import Parser

path = f'./6_ParserASTBuild/eg1.txt'

with open(path, 'r') as file:
    src = file.read()
    
l = Lexer(src)
tokens = l.tokenize()

p = Parser(tokens)
tree = p.parse()
p.print_tree(tree)

