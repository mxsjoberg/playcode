#!/usr/local python3.11

import sys
# print(sys.version)

# tokens
PRINT       = "PRINT"
INTEGER     = "INTEGER"

RESERVED    = [
    "PRINT"
]

class Token(object):
    def __init__(self, m_type, m_value=None):
        self.m_type = m_type
        self.m_value = m_value

    def __repr__(self):
        return f'Token({self.m_type}, {self.m_value})'

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
                if (current_char.isdigit()):
                    number = str(current_char)
                    current_char_index += 1
                    while (source[current_char_index].isdigit() and current_char_index < len(source)):
                        number += str(source[current_char_index])
                        current_char_index += 1
                    tokens.append(Token(INTEGER, number))
                elif (current_char.isalpha()):
                    identifier = str(current_char)
                    current_char_index += 1
                    while (source[current_char_index].isalpha() and current_char_index < len(source)):
                        identifier += str(source[current_char_index])
                        current_char_index += 1
                    if (identifier.upper() in RESERVED):
                        tokens.append(Token(identifier.upper()))
                else:
                    raise Exception("Unknown character.")

    return tokens

source = """
print 42
"""

for token in tokenize(source):
    print(token)
    # Token(PRINT, None)
    # Token(INTEGER, 42)
