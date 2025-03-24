# Lab 3 Report: Lexer & Scanner

### Course: Formal Languages & Finite Automata
### Author: Ivan Rudenco

----

## Theory:
A lexer, or lexical analyzer, is the first stage in the compilation process that transforms source code into meaningful tokens, serving as the bridge between raw text and syntactic structure. It scans the input stream character by character, identifying patterns that match predefined token types like keywords, identifiers, operators, and literals, while discarding whitespace and comments unless specifically preserved. The lexer maintains no understanding of the language's grammar or context; it simply converts the linear sequence of characters into a stream of tokens that will later be consumed by the parser to build a syntactic structure. This separation of concerns between lexical analysis and parsing simplifies compiler design by handling character-level details independently from grammatical rules, making the overall compilation process more modular and maintainable.

## Objectives:

1. Understand what lexical analysis is.
2. Get familiar with the inner workings of a lexer/scanner/tokenizer.
3. Implement a sample lexer and show how it works. 


## Implementation description

I decided to make a lexer for a simplified set of rules for Warhammer 40000 tabletop game. It's a strategy game set in a sci-fi grim-dark setting of Milky way galaxy 40000 years into the future. The game usually operates on turn based engagements between different players, and each of them deploy troops of their chosen faction to fight each other.

The first thing I made was this code example which showcases all of the necessary operations that need to be recognized by the lexer. It defines two players, and each of them choose which troops they deploy while preparing for battle. After the preparations are done, an `engage` loop starts, where players make their moves on a turn by turn scenario.

```
faithful "Roboute Guilliman" {
    deploy space_marines = 50
    deploy chaplain = 1
    deploy dreadnaught = 5

    chaplain cast "Demoralizing Shout"

    dreadnaught vox_transmit "Purge the Heretics!"
}

heretic "Abaddon the Despoiler" {
    deploy warp_horrors = 10
    deploy chaos_sorcerer = 1

    chaos_sorcerer cast "Aura of Terror"
}

engage {
    "Roboute Guilliman"
    "Abaddon the Despoiler"
}
```

To better fit the overall theme of the lexer, I used appropriate names for token types:

```py
class TokenType(Enum):
    faction = 'FACTION'
    str = 'HIGH GOTHIC SPEECH'
    deploy = 'DEPLOY'
    identifyer = 'BRAVE WARRIORS'
    equals = 'BY GOD EMPEROR\'S DECREE'
    num = 'MEN AT ARMS'
    cast = 'CAST'
    vox = 'VOX TRANSMISSION'
    engage = 'FOR THE EMPEROR!'
    lpar = 'IMPERIAL DECREE START'
    rpar = 'IMPERIAL DECREE END'
    invalid = 'TRAITOR'
```

To implement the lexer itself, I made a new Lexer class, which will scan the `src` file and identify all tokens.

```py
class Lexer:
    def __init__(self, src):
        self.src = src
        self.pos = 0
        self.tokens = []
```

I also added several helper methods which are used to identify and handle different types of character sequences. The first one is used to handle strings enclosed within double quotes (`" "`).

```py
def take_str(self):
    self.skip()
    start = self.pos
    while (self.pos < len(self.src) and self.src[self.pos] != '"'):
        self.skip()
    val = self.src[start:self.pos]
```

The second one is used to handle keywords, such as `heretic`, `engage`, etc. All acceptable keywords are stored in the `kws` dictionary.

```py
def take_keyword(self):
    start = self.pos
    while (self.pos < len(self.src) and (self.src[self.pos].isalnum() or self.src[self.pos] == '_')):
        self.skip()
    val = self.src[start:self.pos]
```

The last one is used to identify numbers, such as the amount of units deployed by a player.

```py
def take_num(self):
    start = self.pos
    while (self.pos < len(self.src) and self.src[self.pos].isdigit()):
        self.skip()
    val = self.src[start:self.pos]
```

After a token is identified, it is appended to the end of `tokens` list, which is an attribute of the `Lexer` class. When the whole `src` file is scanned and all tokens are found, the resulting classification can be printed out using `print_tokens` method.

```py
def print_tokens(self):
    for i, token in enumerate(self.tokens):
        print(f"token {i+1:3}   {token}")
```

## Conclusions / Screenshots / Results

The results of tokenizing a valid string will look like this:

```
token   1   type: FACTION                   value: faithful
token   2   type: HIGH GOTHIC SPEECH        value: Roboute Guilliman
token   3   type: IMPERIAL DECREE START     value: {
token   4   type: DEPLOY                    value: deploy
token   5   type: BRAVE WARRIORS            value: space_marines
token   6   type: BY GOD EMPEROR'S DECREE   value: =
token   7   type: MEN AT ARMS               value: 50
token   8   type: DEPLOY                    value: deploy
token   9   type: BRAVE WARRIORS            value: chaplain
token  10   type: BY GOD EMPEROR'S DECREE   value: =
token  11   type: MEN AT ARMS               value: 1
token  12   type: DEPLOY                    value: deploy
token  13   type: BRAVE WARRIORS            value: dreadnaught
token  14   type: BY GOD EMPEROR'S DECREE   value: =
token  15   type: MEN AT ARMS               value: 5
token  16   type: BRAVE WARRIORS            value: chaplain
token  17   type: CAST                      value: cast
token  18   type: HIGH GOTHIC SPEECH        value: Demoralizing Shout
token  19   type: IMPERIAL DECREE END       value: }
```

In conclusion, the lexer was successfully implemented, allowing me to tokenize a simplified Warhammer 40k inspired syntax. The process involved designing meaningful token types, implementing helper functions to handle different lexical elements, and ensuring accurate token classification. Writing the lexer from scratch improved my understanding of lexical analysis and how character sequences are processed into structured tokens. The results demonstrated that the lexer correctly identified keywords, identifiers, numbers, and special symbols, successfully transforming raw input into a token stream. Overall, this lab improved my knowledge of lexer design and gave me hands-on experience in building a fundamental component of a language processor.

## References
- [Warhammer 40000 wiki](https://warhammer40k.fandom.com/wiki/Warhammer_40k_Wiki)
- [good ol' friend](https://chatgpt.com/)