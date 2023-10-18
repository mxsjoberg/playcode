DEBUG = False
RUNNING_TESTS = False

# SYMBOL_TABLE = {}
# TAGS_TABLE = {}

PRINT           = "PRINT"
SWAP            = "SWAP"
IF              = "IF"
ELSE            = "ELSE"
WHILE           = "WHILE"
INTEGER         = "INTEGER"
TRUE            = "TRUE"
FALSE           = "FALSE"
PLUS            = "+"
MINUS           = "-"
MULTIPLY        = "*"
DIVIDE          = "/"
LPAR            = "("
RPAR            = ")"
LBRA            = "{"
RBRA            = "}"
LSBR            = "["
RSBR            = "]"
EQUAL           = "="
EQUALS          = "=="
NOT_EQUALS      = "!="
LESS_THAN       = "<"
GREATER_THAN    = ">"
COMMA           = ","

RESERVED = [
    "PRINT",
    "SWAP",
    "IF",
    "WHILE",
    "ELSE",
    "TRUE",
    "FALSE"
]

COLORS = {
    'header': '\033[95m',
    'blue': '\033[94m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'warning': '\033[93m',
    'fail': '\033[91m',
    'end': '\033[0m',
    'bold': '\033[1m',
    'underline': '\033[4m',
}