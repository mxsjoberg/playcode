#!/usr/local python3.11

import sys
from enum import Enum
# print("Using Python", sys.version.split()[0])

# program       ::= assignment | PRINT expression
# assignment    ::= IDENTIFIER EQUALS expression
# expression    ::= term ((PLUS | MINUS) term)*
# term          ::= factor ((MULTIPLY | DIVIDE) factor)*
# factor        ::= IDENTIFIER | INTEGER | LPAR expression RPAR

# tokens
PRINT       = "PRINT"
INTEGER     = "INTEGER"
PLUS        = "+"
MINUS       = "-"
MULTIPLY    = "*"
DIVIDE      = "/"
LPAR        = "("
RPAR        = ")"
EQUALS      = "=" # PART 2

RESERVED = [
    "PRINT"
]

def print_tree(tree, indent_level=-2):
    if isinstance(tree, list):
        for item in tree:
            print_tree(item, indent_level + 1)
    else:
        indent = '\t' * indent_level
        print(f"{indent}{tree}")

# **** token ****

class TokenType(Enum):
    KEYWORD     = 100
    ASSIGN      = 101 # PART 2
    IDENTIFIER  = 200 # PART 2
    INTEGER     = 201
    PLUS        = 301
    MINUS       = 302
    MULTIPLY    = 304
    DIVIDE      = 305
    LPAR        = 401
    RPAR        = 402
    EQUALS      = 501 # PART 2

class Token(object):
    def __init__(self, m_type, m_value=None):
        self.m_type = m_type
        self.m_value = m_value

    def __repr__(self):
        if self.m_value:
            return f"Token({self.m_type}, '{self.m_value}')"
        else:
            return f"Token({self.m_type})"

# **** lexer ****

# PART 2 START
symbol_table = {}
# PART 2 END

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
                    while source[current_char_index] != '\n':
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
            # PART 2 START
            case '=':
                tokens.append(Token(TokenType.EQUALS, EQUALS))
                current_char_index += 1
            # PART 2 END
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
                    # reserved
                    if identifier.upper() in RESERVED:
                        tokens.append(Token(TokenType.KEYWORD, identifier.upper()))
                    # PART 2 START
                    # variable
                    else:
                        symbol_table[identifier.lower()] = None
                        tokens.append(Token(TokenType.IDENTIFIER, identifier.lower()))
                    # PART 2 END
                else:
                    raise Exception("Unknown character:", current_char)

    return tokens

# **** parser ****

def parse(tokens):
    tree = []
    # ast = {}
    current_token = None
    current_token_index = 0

    while current_token_index < len(tokens):
        program, current_token_index = parse_program(tokens, current_token_index)
        # tree = program
        # ast = program
        tree.append(program)
    # program, current_token_index = parse_program(tokens, current_token_index)
    # tree = program
    # ast = program

    return tree

# program ::= assignment | PRINT expression
def parse_program(tokens, current_token_index):
    program = []
    program_dict = {}
    current_token = tokens[current_token_index]
    current_token_index += 1

    # PART 2 START
    # assignment
    if current_token.m_type == TokenType.IDENTIFIER:
        program.append(Token(TokenType.ASSIGN))
        assignment, current_token_index = parse_assignment(tokens, current_token_index, identifier=current_token)
        program.append(assignment)
    # PART 2 END
    # PRINT
    elif current_token.m_value == PRINT:
        program.append(current_token)
        # expression
        expression, current_token_index = parse_expression(tokens, current_token_index)
        program.append(expression)
    else:
        raise Exception("parse_program", "Unexpected token:", tokens[current_token_index])

    return program, current_token_index

# PART 2 START
# assignment ::= IDENTIFIER EQUALS expression
def parse_assignment(tokens, current_token_index, identifier):
    assignment = []
    # assignment_dict = {}
    current_token = tokens[current_token_index]
    current_token_index += 1

    # EQUALS
    if current_token.m_type == TokenType.EQUALS:
        assignment.append(identifier)
        # expression
        expression, current_token_index = parse_expression(tokens, current_token_index)
        assignment.append(expression)
        symbol_table[identifier.m_value] = expression
    else:
        raise Exception("parse_assignment", "Unexpected token:", tokens[current_token_index])

    return assignment, current_token_index
# PART 2 END

# expression ::= term ((PLUS | MINUS) term)*
def parse_expression(tokens, current_token_index):
    expression = []
    
    # term
    term, current_token_index = parse_term(tokens, current_token_index)
    expression = term

    while current_token_index < len(tokens) and (tokens[current_token_index].m_type == TokenType.PLUS or tokens[current_token_index].m_type == TokenType.MINUS):
        current_token = tokens[current_token_index]
        current_token_index += 1
        match current_token.m_type:
            # PLUS
            case TokenType.PLUS:
                # term
                term, current_token_index = parse_term(tokens, current_token_index)
                expression = [current_token, [expression, term]]
            # MINUS
            case TokenType.MINUS:
                # term
                term, current_token_index = parse_term(tokens, current_token_index)
                expression = [current_token, [expression, term]]
            case _:
                raise Exception("parse_expression", "Unexpected token:", tokens[current_token_index])

    return expression, current_token_index

# term ::= factor ((MULTIPLY | DIVIDE) factor)*
def parse_term(tokens, current_token_index):
    term = []
    
    # factor
    factor, current_token_index = parse_factor(tokens, current_token_index)
    term = factor

    while current_token_index < len(tokens) and (tokens[current_token_index].m_type == TokenType.MULTIPLY or tokens[current_token_index].m_type == TokenType.DIVIDE):
        current_token = tokens[current_token_index]
        current_token_index += 1
        match current_token.m_type:
            # MULTIPLY
            case TokenType.MULTIPLY:
                # factor
                factor, current_token_index = parse_factor(tokens, current_token_index)
                term = [current_token, [term, factor]]
            # DIVIDE
            case TokenType.DIVIDE:
                # factor
                factor, current_token_index = parse_factor(tokens, current_token_index)
                term = [current_token, [term, factor]]
            case _:
                raise Exception("parse_term", "Unexpected token:", tokens[current_token_index])

    return term, current_token_index

# factor ::= IDENTIFIER | INTEGER | LPAR expression RPAR
def parse_factor(tokens, current_token_index):
    factor = []
    current_token = tokens[current_token_index]
    current_token_index += 1
    
    match current_token.m_type:
        # PART 2 START
        # IDENTIFIER
        case TokenType.IDENTIFIER:
            factor = symbol_table[current_token.m_value]
        # PART 2 END
        # INTEGER
        case TokenType.INTEGER:
            factor = current_token
        # LPAR
        case TokenType.LPAR:
            # expression
            expression, current_token_index = parse_expression(tokens, current_token_index)
            factor = expression
            # RPAR
            if current_token_index < len(tokens) and tokens[current_token_index].m_type == TokenType.RPAR:
                current_token_index += 1
            else:
                raise Exception("parse_factor", "Expecting ')':")
        case _:
            raise Exception("parse_factor", "Unexpected token:", tokens[current_token_index])

    return factor, current_token_index

# **** interpreter ****

def interpret(tree):
    result = ''
    node = tree
    if isinstance(node, list):
        left = node[0]
        right = node[1]
    else:
        left = node
        right = None

    match left.m_type:
        case TokenType.KEYWORD if left.m_value == PRINT:
            print(interpret(right))
        case TokenType.PLUS:
            result = int(interpret(right[0])) + int(interpret(right[1]))
        case TokenType.MINUS:
            result = int(interpret(right[0])) - int(interpret(right[1]))
        case TokenType.MULTIPLY:
            result = int(interpret(right[0])) * int(interpret(right[1]))
        case TokenType.DIVIDE:
            result = int(interpret(right[0])) / int(interpret(right[1]))
        # PART 2 START
        case TokenType.INTEGER:
            if left.m_value.isdigit():
                return left.m_value
            else:
                raise Exception("interpret", "Unexpected node:", node)
        case _:
            pass
        # PART 2 END

    return result

# **** main ****

source = """
x = 2
y = 4
print 1 + (x * y) - (6 / x) -> 6
"""

tokens = tokenize(source)
# for token in tokens: print(token)

tree = parse(tokens)
# print(tree)
print_tree(tree)

# print(symbol_table)

for branch in tree:
    interpret(branch)
