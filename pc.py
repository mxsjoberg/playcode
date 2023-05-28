#!/usr/local python3.11

import sys
# print(sys.version)

from enum import Enum

# tokens
PRINT       = "PRINT"
INTEGER     = "INTEGER"

class TokenType(Enum):
    KEYWORD     = 1
    INTEGER     = 2

RESERVED = [
    "PRINT"
]

class Token(object):
    def __init__(self, m_type, m_value):
        self.m_type = m_type
        self.m_value = m_value

    def __repr__(self):
        if self.m_value:
            return f'Token({self.m_type}, {self.m_value})'
        else:
            return f'Token({self.m_type})'

def tokenize(source):
    tokens = []
    current_line = 1
    current_char = ''
    current_char_index = 0

    while current_char_index < len(source):
        current_char = source[current_char_index]
        match current_char:
            case ' ' | '\t' | '\r':
                current_char_index += 1
            case '\n':
                current_line += 1
                current_char_index += 1
            case _:
                if current_char.isdigit():
                    number = str(current_char)
                    current_char_index += 1
                    while source[current_char_index].isdigit() and current_char_index < len(source):
                        number += str(source[current_char_index])
                        current_char_index += 1
                    tokens.append(Token(TokenType.INTEGER, number))
                elif current_char.isalpha():
                    identifier = str(current_char)
                    current_char_index += 1
                    while source[current_char_index].isalpha() and current_char_index < len(source):
                        identifier += str(source[current_char_index])
                        current_char_index += 1
                    if identifier.upper() in RESERVED:
                        tokens.append(Token(TokenType.KEYWORD, identifier.upper()))
                else:
                    raise Exception("Unknown character:", current_char)

    return tokens

def parse(tokens):
    tree = []
    current_token = None
    current_token_index = 0

    while current_token_index < len(tokens):
        program, current_token_index = parse_program(tokens, current_token_index)
        tree.append(program)

    return tree

def parse_program(tokens, current_token_index):
    program = []
    current_token = tokens[current_token_index]
    match current_token.m_type:
        case TokenType.KEYWORD:
            match current_token.m_value:
                case 'PRINT':
                    # PRINT
                    program.append(PRINT)
                    current_token_index += 1
                    # INTEGER
                    factor, current_token_index = parse_factor(tokens, current_token_index)
                    program.append(factor)
                case _:
                    raise Exception("parse_program", "Unexpected token:", tokens[current_token_index])
        case _:
            raise Exception("parse_program", "Unexpected token:", tokens[current_token_index])

    return program, current_token_index

def parse_factor(tokens, current_token_index):
    factor = []
    current_token = tokens[current_token_index]
    match current_token.m_type:
        case TokenType.INTEGER:
            # INTEGER
            factor.append(INTEGER)
            current_token_index += 1
        case _:
            raise Exception("parse_factor", "Unexpected token:", tokens[current_token_index])

    return factor, current_token_index

source = """
print 42
"""

tokens = tokenize(source)
for token in tokens: print(token)

print(parse(tokens))
