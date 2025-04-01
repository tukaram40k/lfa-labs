# Lab 4 Report: Regular expressions

### Course: Formal Languages & Finite Automata
### Author: Ivan Rudenco

----

## Theory:
Regular expressions are sequences of characters used to define search patterns in text processing. They provide a powerful way to match, extract, and manipulate strings based on specific patterns. A regex pattern consists of literal characters and metacharacters, such as `.` (matches any character), `*` (matches zero or more occurrences), `+` (matches one or more occurrences), and `[]` (defines character classes). Anchors like `^` (beginning of a string) and `$` (end of a string) help refine matches. Regex is widely used in programming languages, text editors, and command-line utilities for tasks like data validation, search-and-replace operations, and syntax highlighting. Mastering regular expressions enhances efficiency in handling textual data across various applications.

## Objectives:

1. Write and cover what regular expressions are, what they are used for;

2. Below you will find 3 complex regular expressions per each variant. Take a variant depending on your number in the list of students and do the following:

    a. Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown). Be careful that idea is to interpret the given regular expressions dinamycally, not to hardcode the way it will generate valid strings. You give a set of regexes as input and get valid word as an output

    b. In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations);

    c. **Bonus point**: write a function that will show sequence of processing regular expression (like, what you do first, second and so on)

Write a good report covering all performed actions and faced difficulties.

## Implementation description

I decided to store each regular expression of my vriant (variant 1) as a simple string. These strings can be adjusted to represent other regular expressions, and the program will work with them as well.

```py
re = ['(a|b) (c|d) E+ G?', 'P (Q|R|S) T (UV|W|X)* Z+', '1 (0|1)* 2 (3|4)5 36']
```

In order to extract the regular expression from the strings, I made a simple scanner using python's `re` module, that consists of two methods. The first one splits each string into smaller token-like parts, which can be used later:

```py
def scan_re(self):
    self.reg = [re.split(' ', i) for i in self.src]
```

The second method goes through each identified token and performs the necessary operations to determine which operation should be done.

```py
def get_str(self):
    strings = []
    
    for reg in self.reg:
        str = []
        
        for token in reg:
            result = []
```

This part handles the repeat operations, such as 0 or 1 repetition (`?`), 0 or more repetitions (`*`), and 1 or more repetitions (`+`). The identified operation is stored in the `last` variable and is used later to determine how many times the symbols repeat.

```py
# check for *,+,?
last = token[-1]
if last == ')':
    last = '1'
    chars = (token + '.')[:-1]
elif last in ['*', '+', '?']: chars = token[:-1]
else: chars = (token + '.')[:-1]
```

This part identifies isolated characters that don't belong to a group (i.e. `'P'`), removes leftover parentheses and sets repetition number to `1`.

```py
if last.isalpha(): last = '1'
if ')' in chars and last.isdigit(): chars = chars[:-1]
if '(' not in chars and ')' not in chars and last not in ['*', '+', '?']: last = '1'

chars = chars.replace('(', '')
chars = chars.replace(')', '')
```

To handle the `|` operation, the string is split once again, and a randomly chosen option is added to the result. Then, the symbol is repeated a number of times, based on the the `last` variable created in the previous steps.

```py
chars = chars.split('|')

if last.isdigit():
    ch = r.choice(chars)
    for _ in range(int(last)):
        result.append(ch)
```

Lastly, repetition is handled, and the symbols are repeated 0 or 1 time in case of `?`, 0 or more times in case of `*`, and 1 or more times in case of `+`. To prevent generation of very long strings, the maximum number of repetitions is capped at 5.

```py
elif last == '?':
    if r.randint(0, 1) == 1:
        result.append(r.choice(chars))
elif last == '+':
    ch = r.choice(chars)
    for _ in range(r.randint(1, 5)):
        result.append(ch)
elif last == '*':
    ch = r.choice(chars)
    for _ in range(r.randint(0, 5)):
        result.append(ch)
```

To better show how string generation works, I made a helper method that generates and prints `n` unique strings for each given regular expression.

```py
def generate_str(self, n):
    results = []
    
    while len(results) < n:
        str = self.get_str()
        if str not in results: results.append(str)
```

## Conclusions / Screenshots / Results

The results of generating 5 valid string according to my variant will look like this:

```
['acEEG', 'PSTUVUVUVUVZZZZ', '11124444436']
['acEEEEEG', 'PRTXZZZZZ', '111123333336']
['bdE', 'PSTZZZZ', '1024444436']
['bdEG', 'PSTWZZZZ', '1111123333336']
['bcEEG', 'PRTUVUVUVUVUVZZ', '1111123333336']
```

In conclusion, this lab was a great hands-on experience with regular expressions, showing how they can be used dynamically to generate valid strings. By breaking down each regex pattern into smaller parts and applying the correct operations, the program successfully produced strings that matched the given rules. One of the biggest challenges was correctly handling repetition operators like *, +, and ?, and correctly identifying which group of characters they belong to. Despite some trial and error, the final implementation worked well, generating accurate outputs that. Overall, this lab helped me better undersnand regex in text processing and gave me a deeper understanding of how to find string patterns programmatically.

## References
- [good ol' friend](https://chatgpt.com/)