SPECIFICATION_GRAMMAR = """
S -> label SP '=' SP def
SP -> ' '
def -> label | string | ascii | OR | opt | comment | group
group -> '(' def ')' | multi '(' def ')'
comment -> def SP ';' SP name
opt -> '[' def ']'
OR -> def SP '/' SP def
multi -> '*' | number | number '*' number | number '*'
label -> name
string -> '"' name '"'
ascii -> '%' 'x' hex hex | '%' 'x' hex hex '-' hex hex
number -> '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | number number
hex -> 'A' | 'a' | 'B' | 'b' | 'C' | 'c' | 'D' | 'd' | 'E' | 'e' | 'F' | 'f' | number
name -> name char | char
symbol -> '=' | '<' | ':' | '+' | '|' | '#' | ',' | '{' | '}' | '.'
char -> 'A' | 'a' | 'B' | 'b' | 'C' | 'c' | 'D' | 'd' | 'E' | 'e' | 'F' | 'f' | 'G' | 'g' | 'H' | 'h' | 'I' | 'i' | 'J' | 'j' | 'K' | 'k' | 'L' | 'l' | 'M' | 'm' | 'N' | 'n' | 'O' | 'o' | 'P' | 'p' | 'Q' | 'q' | 'R' | 'r' | 'S' | 's' | 'T' | 't' | 'U' | 'u' | 'V' | 'v' | 'W' | 'w' | 'X' | 'x' | 'Y' | 'y' | 'Z' | 'z' | symbol
"""