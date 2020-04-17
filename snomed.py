import pathlib

SPECIFICATION_GRAMMAR = """
S -> label SP '=' SP def
SP -> ' '
def -> label | string | ascii | OR | opt | comment | group
group -> '(' def ')' | multi '(' def ')'
comment -> def SP ';' SP words
opt -> '[' def ']'
OR -> def SP '/' SP def
multi -> '*' | number | number '*' number | number '*'
label -> word
string -> '"' word '"'
ascii -> '%' 'x' hex hex | '%' 'x' hex hex '-' hex hex
number -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | number number
hex -> 'A' | 'a' | 'B' | 'b' | 'C' | 'c' | 'D' | 'd' | 'E' | 'e' | 'F' | 'f' | number
words -> words SP word | word
word -> chars
symbol -> '=' | '<' | ':' | '+' | '|' | '#' | ',' | '{' | '}' | '.'
chars -> chars char | char
char -> 'A' | 'a' | 'B' | 'b' | 'C' | 'c' | 'D' | 'd' | 'E' | 'e' | 'F' | 'f' | 'G' | 'g' | 'H' | 'h' | 'I' | 'i' | 'J' | 'j' | 'K' | 'k' | 'L' | 'l' | 'M' | 'm' | 'N' | 'n' | 'O' | 'o' | 'P' | 'p' | 'Q' | 'q' | 'R' | 'r' | 'S' | 's' | 'T' | 't' | 'U' | 'u' | 'V' | 'v' | 'W' | 'w' | 'X' | 'x' | 'Y' | 'y' | 'Z' | 'z' | symbol
"""


def read_spec(file):
    spec = pathlib.Path(file).read_text()
    spec = [' '.join(line.split()) for line in spec.splitlines()]
    return spec
