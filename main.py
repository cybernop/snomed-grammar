import pathlib
import nltk
import re

spec = pathlib.Path('grammar.txt').read_text()

spec = spec.splitlines()

grammar = nltk.CFG.fromstring("""
rule -> symbol SP ' = ' SP def
SP -> ' '
def -> symbol | string | ascii | OR | opt | comment | group | def SP def
group -> '(' def ')' | multi '(' def ')'
comment -> def SP ';' SP name
opt -> '[' def ']'
OR -> def SP '/' SP def
multi -> '*' | number | number '*' number | number '*'
symbol -> name
string -> '"' name '"'
ascii -> '%' 'x' hex hex | '%' 'x' hex hex '-' hex hex
number -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | number number
hex -> 'A' | 'a' | 'B' | 'b' | 'C' | 'c' | 'D' | 'd' | 'E' | 'e' | 'F' | 'f' | number
name -> name char | char
symbol -> '=' | '<' | ':' | '+' | '|' | '#' | ',' | '{' | '}' | '.'
char -> 'A' | 'a' | 'B' | 'b' | 'C' | 'c' | 'D' | 'd' | 'E' | 'e' | 'F' | 'f' | 'G' | 'g' | 'H' | 'h' | 'I' | 'i' | 'J' | 'j' | 'K' | 'k' | 'L' | 'l' | 'M' | 'm' | 'N' | 'n' | 'O' | 'o' | 'P' | 'p' | 'Q' | 'q' | 'R' | 'r' | 'S' | 's' | 'T' | 't' | 'U' | 'u' | 'V' | 'v' | 'W' | 'w' | 'X' | 'x' | 'Y' | 'y' | 'Z' | 'z' | symbol
""")

parser = nltk.ChartParser(grammar)


entries = [
    # 'equivalentTo = "==="',
    # 'subtypeOf = "<<<"',
    'foo = a',
    'conceptId = sctId',
    'definitionStatus = equivalentTo / subtypeOf',
    # 'expression =  ws [definitionStatus ws] subExpression ws'
]

# for entry in entries:
#     for tree in parser.parse(entry):
#         tree.pretty_print()

trees = []
for i, entry in enumerate(spec):
    try:
        for tree in parser.parse(entry):
            tree.pretty_print()
            trees.append(tree)
    except ValueError as e:
        print(f'{i}: {entry}: {e}')

spec = spec.replace(' = ',  ' -> ')
spec = spec.replace('\"', '\'')
spec = spec.replace('/', '|')

# remove comments
spec = [entry.split(' ; ')[0] for entry in spec]

# handle acsii
spec = [re.sub(r'(%x[A-F0-9]{2}(-\w{2})?)', '\'\\1\'', entry) for entry in spec]

# handle optional parts
optional_re = re.compile(r' \[(.+)\]')
new_entries = []
remove_entries = []
for entry in spec:
    match = optional_re.search(entry)
    if match:
        new_entries.append(entry.replace(match[0], ''))
        new_entries.append(entry.replace(match[0], f' ({match[1]})'))
        remove_entries.append(entry)

for entry in remove_entries:
    spec.remove(entry)

spec += new_entries

spec.sort()

print('foo')
