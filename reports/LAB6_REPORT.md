# Lab 5 Report: Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Ivan Rudenco

----

## Theory:
A parser is the second stage in the compilation process that follows lexical analysis. While a lexer breaks down raw text into tokens, a parser analyzes these tokens according to a grammar, determining their structural relationships and constructing an Abstract Syntax Tree (AST). The AST represents the hierarchical structure of the program, where each node corresponds to a construct in the source code. This tree structure facilitates semantic analysis, optimization, and code generation in later compilation stages. The parser's role is crucial as it transforms the flat sequence of tokens into a structured representation that reflects the logical organization and meaning of the program, making it possible to understand and manipulate the code at a higher level of abstraction.

## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.


## Implementation description

Building upon the lexer from the previous lab, I implemented a parser and AST for the same Warhammer 40k-themed language. 

### 1. AST nodes
I defined several AST node classes to represent different language constructs:

```py
class AstNode:
    def tree_str(self, indent=0, prefix=""):
        raise NotImplementedError

class FactionDeclaration(AstNode):
    def __init__(self, faction_type, leader_name, body):
        self.faction_type = faction_type
        self.leader_name = leader_name
        self.body = body

class DeploymentStmt(AstNode):
    def __init__(self, unit_type, count):
        self.unit_type = unit_type
        self.count = count
```

One class is defined for each feature of the language: faction, deployment, cast, vox, engagement, and army.
Each node has a method to generate its string representation:

```py
def tree_str(self, indent=0, prefix=""):
    spaces = '    ' * indent
    return f"{spaces}{prefix}Deploy: {self.unit_type}, {self.count}\n"
```

### 2. Parser

The parser itself is implemented as a class that takes a list of tokens and builds an AST:

```py
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = None
        self.pos = -1
        self.advance()
```

Parser goes through list of tokens, and builds AST with separate methods for each language construct:

```py
def parse(self):
    ast = []
    while self.current_token and self.current_token.type != TokenType.eof:
        if self.current_token.type == TokenType.faction:
            ast.append(self.parse_faction())
        elif self.current_token.type == TokenType.engage:
            ast.append(self.parse_engagement())
        else:
            raise SyntaxError(f"UNEXPECTED COMMAND: {self.current_token.value} (type: {self.current_token.type.value})")
    return ast
```

Declaration of faction and its leader is handled by `parse_faction()` method:

```py
def parse_faction(self):
    faction_type = self.expect(TokenType.faction, "Expected faction declaration")
    leader_name = self.expect(TokenType.str, "Expected leader name in high gothic")
    self.expect(TokenType.lpar, "Expected '{' to begin faction block")

```

Deployment of forces is handled by `parse_deployment()` method:

```py
def parse_deployment(self):
    self.expect(TokenType.deploy, "Expected 'deploy' command")
    unit_type = self.expect(TokenType.identifier, "Expected unit type")
    self.expect(TokenType.equals, "Expected '=' in deployment")
    count = self.expect(TokenType.num, "Expected unit count")
    return DeploymentStmt(unit_type, count)
```

Using an ability or spell is handled by `parse_cast()` method:

```py
def parse_cast(self, unit_name=None):
    if unit_name is None:
        unit_name = self.expect(TokenType.identifier, "Expected caster identifier")
    self.expect(TokenType.cast, "Expected 'cast' command")
    ability = self.expect(TokenType.str, "Expected ability name in high gothic")
    return CastStmt(unit_name, ability)
```

Starting a battle is handled by `parse_cast()` method:

```py
def parse_engagement(self):
    self.expect(TokenType.engage, "Expected 'engage' command")
    self.expect(TokenType.lpar, "Expected '{' to begin engagement block")
    
    combatants = []
    while self.current_token and self.current_token.type != TokenType.rpar:
        combatant = self.expect(TokenType.str, "Expected combatant name in high gothic")
        combatants.append(combatant)
```

After code is parsed and AST is obtained, it can be printed to console:

```py
def print_tree(self, tree):
    print("\nBattle Start")
    for i, node in enumerate(tree):
        print(node.tree_str(1, "|__ "))
```

## Conclusions / Screenshots / Results

Example code for parsing:

```
faithful "Roboute Guilliman" {
    deploy space_marines = 50
    chaplain cast "Demoralizing Shout"
}

heretic "Abaddon the Despoiler" {
    deploy warp_horrors = 10
}

engage {
    "Roboute Guilliman"
    "Abaddon the Despoiler"
}
```

Running the lexer and parser on the example code will generate the following Abstract Syntax Tree:

```
Battle Start
    |__ Hero: faithful, Roboute Guilliman
        |__ Army:
            |__ Deploy: space_marines, 50
            |__ Cast: chaplain, "Demoralizing Shout"
    |__ Hero: heretic, Abaddon the Despoiler
        |__ Army:
            |__ Deploy: warp_horrors, 10
    |__ Engagement
        |__ Hero: "Roboute Guilliman"
        |__ Hero: "Abaddon the Despoiler"
```

In conclusion, I successfully implemented a parser that builds an AST for a simplified Warhammer 40k language. The parser correctly handles the different language constructs and their relationships. The AST provides a clear representation of the program structure, which could be used for further processing or interpretation.
This lab improved my understanding of parsing and abstract syntax trees. I learned how to transform a linear sequence of tokens into a hierarchical structure that reflects the logical organization of a program. I also gained experience in effective error handling, since I was getting a lot of errors during the development of the parser.

## References
- [Warhammer 40000 wiki](https://warhammer40k.fandom.com/wiki/Warhammer_40k_Wiki)
- [good ol' friend](https://chatgpt.com/)
