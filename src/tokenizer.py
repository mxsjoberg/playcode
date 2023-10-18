from src.consts import *
from src.token import *

TAGS_TABLE = {}

# **** tokenizer ****
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
            case '+':
                tokens.append(Token(TokenType.PLUS, PLUS))
                current_char_index += 1
            case '-':
                # comments
                next_char = source[current_char_index + 1]
                if next_char == '-' or next_char == '>':
                    current_char_index += 1
                    # skip until newline
                    while current_char_index < len(source) and source[current_char_index] != '\n':
                        current_char_index += 1
                # minus
                else:
                    tokens.append(Token(TokenType.MINUS, MINUS))
                    current_char_index += 1
            case '*':
                tokens.append(Token(TokenType.MULTIPLY, MULTIPLY))
                current_char_index += 1
            case '/':
                tokens.append(Token(TokenType.DIVIDE, DIVIDE))
                current_char_index += 1
            case '(':
                tokens.append(Token(TokenType.LPAR, LPAR))
                current_char_index += 1
            case ')':
                tokens.append(Token(TokenType.RPAR, RPAR))
                current_char_index += 1
            case '{':
                tokens.append(Token(TokenType.LBRA, LBRA))
                current_char_index += 1
            case '}':
                tokens.append(Token(TokenType.RBRA, RBRA))
                current_char_index += 1
            case '[':
                tokens.append(Token(TokenType.LSBR, LSBR))
                current_char_index += 1
            case ']':
                tokens.append(Token(TokenType.RSBR, RSBR))
                current_char_index += 1
            case '=':
                # equals
                next_char = source[current_char_index + 1]
                if next_char == '=':
                    tokens.append(Token(TokenType.EQUALS, EQUALS))
                    current_char_index += 2
                # equal
                else:
                    tokens.append(Token(TokenType.EQUAL, EQUAL))
                    current_char_index += 1
            case '!':
                # not equals
                next_char = source[current_char_index + 1]
                if next_char == '=':
                    tokens.append(Token(TokenType.NOT_EQUALS, NOT_EQUALS))
                    current_char_index += 2
                else:
                    raise Exception("Unknown character:", current_char)
            case '<':
                tokens.append(Token(TokenType.LESS_THAN, LESS_THAN))
                current_char_index += 1
            case '>':
                tokens.append(Token(TokenType.GREATER_THAN, GREATER_THAN))
                current_char_index += 1
            case '@':
                identifier = ""
                current_char_index += 1
                while current_char_index < len(source) and source[current_char_index].isalpha():
                    identifier += str(source[current_char_index])
                    current_char_index += 1
                TAGS_TABLE[identifier.lower()] = None
                tokens.append(Token(TokenType.TAG, identifier.lower()))
                if source[current_char_index] == '\n':
                    tokens.append(Token(TokenType.EMPTY))
            case ',':
                tokens.append(Token(TokenType.COMMA, COMMA))
                current_char_index += 1
            case _:
                if current_char.isdigit():
                    number = str(current_char)
                    current_char_index += 1
                    while current_char_index < len(source) and source[current_char_index].isdigit():
                        number += str(source[current_char_index])
                        current_char_index += 1
                    tokens.append(Token(TokenType.INTEGER, number))
                elif current_char.isalpha():
                    identifier = str(current_char)
                    current_char_index += 1
                    while current_char_index < len(source) and source[current_char_index].isalpha():
                        identifier += str(source[current_char_index])
                        current_char_index += 1
                    # boolean
                    if identifier.upper() == "TRUE" or identifier.upper() == "FALSE":
                        tokens.append(Token(TokenType.BOOLEAN, identifier.upper()))
                    # reserved
                    elif identifier.upper() in RESERVED:
                        tokens.append(Token(TokenType.KEYWORD, identifier.upper()))
                    # identifier
                    else:
                        tokens.append(Token(TokenType.IDENTIFIER, identifier.lower()))
                else:
                    raise Exception("Unknown character:", current_char)

    return tokens
