from lexer import Lexer
from pathlib import Path

dir = Path(__file__).parent # че за говно

with open(f'{dir}/eg1.txt', 'r') as file:
    text = file.read()
    
    l1 = Lexer(text)
    l1.tokenize()
    l1.print_tokens()