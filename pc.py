#!/usr/local python3.11

import sys
from enum import Enum
# print("Using Python", sys.version.split()[0])

# program           ::= assignment | swap_statement | if_statement | PRINT comparison
# assignment        ::= IDENTIFIER EQUAL expression
# tag_statement     ::= TAG program
# swap_statement    ::= SWAP IDENTIFIER IDENTIFIER
# if_statement      ::= IF comparison LBRA program RBRA (ELSE LBRA program RBRA)?
# comparison        ::= expression ((EQUALS | NOT_EQUALS | LESS_THAN | GREATER_THAN) expression)*
# expression        ::= term ((PLUS | MINUS) term)*
# term              ::= factor ((MULTIPLY | DIVIDE) factor)*
# factor            ::= IDENTIFIER | BOOLEAN | INTEGER | LPAR expression RPAR

# tokens
PRINT       = "PRINT"
SWAP        = "SWAP"
IF          = "IF"
ELSE        = "ELSE"
INTEGER     = "INTEGER"
TRUE        = "TRUE"
FALSE       = "FALSE"
PLUS        = "+"
MINUS       = "-"
MULTIPLY    = "*"
DIVIDE      = "/"
LPAR        = "("
RPAR        = ")"
LBRA        = "{"
RBRA        = "}"
EQUAL       = "="
EQUALS      = "=="
NOT_EQUALS  = "!="
LESS_THAN   = "<"
GREATER_THAN= ">"

RESERVED = [
    "PRINT",
    "SWAP",
    "IF",
    "ELSE",
    "TRUE",
    "FALSE"
]

def print_tree(tree, indent_level=-2):
    if isinstance(tree, list):
        for item in tree:
            if len(tree) > 1:
                print_tree(item, indent_level + 1)
            else:
                print_tree(item, indent_level)
    else:
        if tree.m_type == TokenType.INTEGER or tree.m_type == TokenType.BOOLEAN:
            indent_level = indent_level + 1
        indent = '\t' * indent_level
        print(f"{indent}{tree}")

class TokenType(Enum):
    KEYWORD         = 100
    ASSIGN          = 101
    EMPTY           = 102
    IDENTIFIER      = 200
    INTEGER         = 201
    BOOLEAN         = 202
    TAG             = 203
    PLUS            = 301
    MINUS           = 302
    MULTIPLY        = 304
    DIVIDE          = 305
    EQUALS          = 306
    NOT_EQUALS      = 307
    LESS_THAN       = 308
    GREATER_THAN    = 309
    LPAR            = 401
    RPAR            = 402
    LBRA            = 403
    RBRA            = 404
    EQUAL           = 501

class Token(object):
    def __init__(self, m_type, m_value=None):
        self.m_type = m_type
        self.m_value = m_value

    def __repr__(self):
        if self.m_value:
            return f"Token({self.m_type}, '{self.m_value}')"
        else:
            return f"Token({self.m_type})"

symbol_table = {}

tags_table = {}

# **** lexer ****

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
            case '{':
                tokens.append(Token(TokenType.LBRA, LBRA))
                current_char_index += 1
            case '}':
                tokens.append(Token(TokenType.RBRA, RBRA))
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
                while source[current_char_index].isalpha() and current_char_index < len(source):
                    identifier += str(source[current_char_index])
                    current_char_index += 1
                tags_table[identifier.lower()] = None
                tokens.append(Token(TokenType.TAG, identifier.lower()))
                if source[current_char_index] == '\n':
                    tokens.append(Token(TokenType.EMPTY))
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
                    # boolean
                    if identifier.upper() == "TRUE" or identifier.upper() == "FALSE":
                        tokens.append(Token(TokenType.BOOLEAN, identifier.upper()))
                    # reserved
                    elif identifier.upper() in RESERVED:
                        tokens.append(Token(TokenType.KEYWORD, identifier.upper()))
                    # identifier
                    else:
                        symbol_table[identifier.lower()] = None
                        tokens.append(Token(TokenType.IDENTIFIER, identifier.lower()))
                else:
                    raise Exception("Unknown character:", current_char)

    return tokens

# **** parser ****

def parse(tokens):
    tree = []
    current_token = None
    current_token_index = 0

    while current_token_index < len(tokens):
        program, current_token_index = parse_program(tokens, current_token_index)
        tree.append(program)

    return tree

# program ::= assignment | tag_statement | swap_statement | if_statement | PRINT comparison
def parse_program(tokens, current_token_index):
    program = []
    program_dict = {}
    current_token = tokens[current_token_index]
    current_token_index += 1

    # assignment
    if current_token.m_type == TokenType.IDENTIFIER:
        program.append(Token(TokenType.ASSIGN))
        assignment, current_token_index = parse_assignment(tokens, current_token_index, identifier=current_token)
        program.append(assignment)
    # tag_statement
    elif current_token.m_type == TokenType.TAG:
        program.append(Token(TokenType.TAG, current_token.m_value))
        tag_statement, current_token_index = parse_tag_statement(tokens, current_token_index, identifier=current_token)
        program.append(tag_statement)
    # swap_statement
    elif current_token.m_value == SWAP:
        program.append(current_token)
        swap_statement, current_token_index = parse_swap_statement(tokens, current_token_index)
        program.append(swap_statement)
    # if_statement
    elif current_token.m_value == IF:
        program.append(current_token)
        if_statement, current_token_index = parse_if_statement(tokens, current_token_index)
        program.append(if_statement)
    # PRINT
    elif current_token.m_value == PRINT:
        program.append(current_token)
        # expression
        expression, current_token_index = parse_comparison(tokens, current_token_index)
        program.append(expression)
    else:
        raise Exception("parse_program", "Unexpected token:", tokens[current_token_index])

    return program, current_token_index

# assignment ::= IDENTIFIER EQUAL expression
def parse_assignment(tokens, current_token_index, identifier):
    assignment = []
    current_token = tokens[current_token_index]
    current_token_index += 1

    # EQUAL
    if current_token.m_type == TokenType.EQUAL:
        assignment.append(identifier)
        # expression
        expression, current_token_index = parse_expression(tokens, current_token_index)
        assignment.append(expression)
        symbol_table[identifier.m_value] = expression
    else:
        raise Exception("parse_assignment", "Unexpected token:", tokens[current_token_index])

    return assignment, current_token_index

# tag_statement ::= TAG (EMPTY | program)+
def parse_tag_statement(tokens, current_token_index, identifier):
    tag_statement = []

    # EMPTY
    if tokens[current_token_index].m_type == TokenType.EMPTY:
        current_token_index += 1
    # program
    else:
        program, current_token_index = parse_program(tokens, current_token_index)
        tag_statement.append(program)
        tags_table[identifier.m_value] = program

    return tag_statement, current_token_index

# swap_statement ::= SWAP IDENTIFIER IDENTIFIER
def parse_swap_statement(tokens, current_token_index):
    swap_statement = []
    current_token = tokens[current_token_index]
    current_token_index += 1

    # IDENTIFIER
    if current_token.m_type == TokenType.IDENTIFIER:
        swap_statement.append(current_token)
        # IDENTIFIER
        current_token = tokens[current_token_index]
        current_token_index += 1
        if current_token.m_type == TokenType.IDENTIFIER:
            swap_statement.append(current_token)
        else:
            raise Exception("parse_swap_statement", "Unexpected token:", tokens[current_token_index])
    else:
        raise Exception("parse_swap_statement", "Unexpected token:", tokens[current_token_index])

    return swap_statement, current_token_index

# if_statement ::= IF comparison LBRA program RBRA (ELSE LBRA program RBRA)?
def parse_if_statement(tokens, current_token_index):
    if_statement = []
    # comparison
    comparison, current_token_index = parse_comparison(tokens, current_token_index)
    if_statement.append(comparison)

    # LBRA
    current_token = tokens[current_token_index]
    current_token_index += 1
    if current_token.m_type == TokenType.LBRA:
        # program
        program, current_token_index = parse_program(tokens, current_token_index)
        if_statement.append(program)
        # RBRA
        current_token = tokens[current_token_index]
        current_token_index += 1
        if current_token.m_type == TokenType.RBRA:
            pass
        else:
            raise Exception("parse_if_statement", "Unexpected token:", tokens[current_token_index])
    else:
        raise Exception("parse_if_statement", "Unexpected token:", tokens[current_token_index])
    # (ELSE LBRA program RBRA)?
    if current_token_index < len(tokens) and tokens[current_token_index].m_value == ELSE:
        # ELSE
        current_token = tokens[current_token_index]
        current_token_index += 1
        # LBRA
        current_token = tokens[current_token_index]
        current_token_index += 1
        if current_token.m_type == TokenType.LBRA:
            # program
            program, current_token_index = parse_program(tokens, current_token_index)
            if_statement.append(program)
            # RBRA
            current_token = tokens[current_token_index]
            current_token_index += 1
            if current_token.m_type == TokenType.RBRA:
                pass
            else:
                raise Exception("parse_if_statement", "Unexpected token:", tokens[current_token_index])
        else:
            raise Exception("parse_if_statement", "Unexpected token:", tokens[current_token_index])
    else:
        if_statement.append(Token(TokenType.EMPTY))

    return if_statement, current_token_index

# comparison ::= expression ((EQUALS | NOT_EQUALS | LESS_THAN | GREATER_THAN) expression)*
def parse_comparison(tokens, current_token_index):
    comparison = []
    # expression
    expression, current_token_index = parse_expression(tokens, current_token_index)
    comparison = expression

    while current_token_index < len(tokens) and (tokens[current_token_index].m_type == TokenType.EQUALS or tokens[current_token_index].m_type == TokenType.NOT_EQUALS or tokens[current_token_index].m_type == TokenType.LESS_THAN or tokens[current_token_index].m_type == TokenType.GREATER_THAN):
        current_token = tokens[current_token_index]
        current_token_index += 1
        match current_token.m_type:
            # EQUALS
            case TokenType.EQUALS:
                # expression
                expression, current_token_index = parse_expression(tokens, current_token_index)
                comparison = [current_token, [comparison, expression]]
            # NOT_EQUALS
            case TokenType.NOT_EQUALS:
                # expression
                expression, current_token_index = parse_expression(tokens, current_token_index)
                comparison = [current_token, [comparison, expression]]
            # LESS_THAN
            case TokenType.LESS_THAN:
                # expression
                expression, current_token_index = parse_expression(tokens, current_token_index)
                comparison = [current_token, [comparison, expression]]
            # GREATER_THAN
            case TokenType.GREATER_THAN:
                # expression
                expression, current_token_index = parse_expression(tokens, current_token_index)
                comparison = [current_token, [comparison, expression]]

    return comparison, current_token_index

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

# factor ::= IDENTIFIER | BOOLEAN | INTEGER | LPAR expression RPAR
def parse_factor(tokens, current_token_index):
    factor = []
    current_token = tokens[current_token_index]
    current_token_index += 1
    
    match current_token.m_type:
        # IDENTIFIER
        case TokenType.IDENTIFIER:
            factor = current_token
        # BOOLEAN
        case TokenType.BOOLEAN:
            factor = current_token
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
        # PRINT
        case TokenType.KEYWORD if left.m_value == PRINT:
            print(interpret(right))
        # SWAP
        case TokenType.KEYWORD if left.m_value == SWAP:
            symbol_table[right[0].m_value], symbol_table[right[1].m_value] = symbol_table[right[1].m_value], symbol_table[right[0].m_value]
        # IF
        case TokenType.KEYWORD if left.m_value == IF:
            if interpret(right[0]):
                interpret(right[1])
            else:
                interpret(right[2])
        # TAG
        case TokenType.TAG:
            return interpret(tags_table[left.m_value])
        # identifier
        case TokenType.IDENTIFIER:
            return interpret(symbol_table[left.m_value])
        # PLUS
        case TokenType.PLUS:
            result = int(interpret(right[0])) + int(interpret(right[1]))
        # MINUS
        case TokenType.MINUS:
            result = int(interpret(right[0])) - int(interpret(right[1]))
        # MULTIPLY
        case TokenType.MULTIPLY:
            result = int(interpret(right[0])) * int(interpret(right[1]))
        # DIVIDE
        case TokenType.DIVIDE:
            result = int(interpret(right[0])) / int(interpret(right[1]))
        # EQUALS
        case TokenType.EQUALS:
            result = int(interpret(right[0])) == int(interpret(right[1]))
        # NOT_EQUALS
        case TokenType.NOT_EQUALS:
            result = int(interpret(right[0])) != int(interpret(right[1]))
        # LESS_THAN
        case TokenType.LESS_THAN:
            result = int(interpret(right[0])) < int(interpret(right[1]))
        # GREATER_THAN
        case TokenType.GREATER_THAN:
            result = int(interpret(right[0])) > int(interpret(right[1]))
        # INTEGER
        case TokenType.INTEGER:
            return left.m_value
        # BOOLEAN
        case TokenType.BOOLEAN:
            if left.m_value == TRUE:
                return True
            elif left.m_value == FALSE:
                return False
        case _:
            pass

    return result

# **** main ****

# source = """
# x = 2 * 2
# y = 2
# -- swap
# swap x y
# -- print
# print 1 + (x * y) - (6 / x) -> 6
# """

# source = """
# x = 2
# if x > 0 {
#     print True
# } else {
#     print False
# }
# """

source = """
@print print 42
@print
"""

tokens = tokenize(source)
# for token in tokens: print(token)

tree = parse(tokens)
# print(tree)
print_tree(tree)

for branch in tree:
    interpret(branch)

# print(symbol_table)
print(tags_table)
