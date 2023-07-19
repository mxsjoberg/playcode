#!/usr/local python3.11

import os
import sys
from enum import Enum
# print("Using Python", sys.version.split()[0])

DEBUG = False
RUNNING_TESTS = False

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

# program           ::= assignment | swap_statement | if_statement | while_statement | PRINT comparison
# assignment        ::= IDENTIFIER (LSBR expression RSBR)? EQUAL (vector | expression)+
# tag_statement     ::= TAG (EMPTY | program)+
# swap_statement    ::= SWAP IDENTIFIER (LSBR expression RSBR)? IDENTIFIER (LSBR expression RSBR)?
# if_statement      ::= IF comparison LBRA (program)* RBRA (ELSE LBRA (program)* RBRA)?
# while_statement   ::= WHILE comparison LBRA (program)* RBRA
# comparison        ::= expression ((EQUALS | NOT_EQUALS | LESS_THAN | GREATER_THAN) expression)*
# expression        ::= term ((PLUS | MINUS) term)*
# term              ::= factor ((MULTIPLY | DIVIDE) factor)*
# factor            ::= IDENTIFIER (LSBR expression RSBR)? | BOOLEAN | INTEGER | LPAR expression RPAR
# vector            ::= LSBR (expression (COMMA expression)*)? RSBR

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

def print_tree(tree, indent_level=-2):
    if isinstance(tree, list):
        for item in tree:
            if len(tree) > 1:
                print_tree(item, indent_level + 1)
            else:
                print_tree(item, indent_level)
    else:
        indent = '  ' * indent_level
        print(f"{indent}{tree}")

class TokenType(Enum):
    KEYWORD         = 100
    ASSIGN          = 101
    INDEX           = 102
    EMPTY           = 103
    IDENTIFIER      = 200
    INTEGER         = 201
    VECTOR          = 202
    BOOLEAN         = 203
    TAG             = 204
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
    LSBR            = 405
    RSBR            = 406
    EQUAL           = 501
    COMMA           = 502

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
                tags_table[identifier.lower()] = None
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

# **** parser ****
def parse(tokens):
    tree = []
    current_token = None
    current_token_index = 0

    while current_token_index < len(tokens):
        program, current_token_index = parse_program(tokens, current_token_index)
        tree.append(program)

    return tree

# program ::= assignment | tag_statement | swap_statement | if_statement | while_statement | PRINT comparison
def parse_program(tokens, current_token_index):
    if DEBUG: print(f"{COLORS['warning']}parse_program{COLORS['end']}")
    program = []
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
    # while_statement
    elif current_token.m_value == WHILE:
        program.append(current_token)
        while_statement, current_token_index = parse_while_statement(tokens, current_token_index)
        program.append(while_statement)
    # PRINT
    elif current_token.m_value == PRINT:
        program.append(current_token)
        # expression
        expression, current_token_index = parse_comparison(tokens, current_token_index)
        program.append(expression)
    else:
        raise Exception("parse_program", "Unexpected token:", tokens[current_token_index])

    return program, current_token_index

# assignment ::= IDENTIFIER (LSBR expression RSBR)? EQUAL (vector | expression)+
def parse_assignment(tokens, current_token_index, identifier):
    if DEBUG: print(f"{COLORS['warning']}parse_assignment{COLORS['end']}")
    assignment = []
    current_token = tokens[current_token_index]
    current_token_index += 1
    # LSBR
    if current_token_index < len(tokens) and current_token.m_type == TokenType.LSBR:
        # expression
        expression, current_token_index = parse_expression(tokens, current_token_index)
        assignment.append([identifier, expression])
        # RSBR
        current_token = tokens[current_token_index]
        current_token_index += 1
        if current_token.m_type == TokenType.RSBR:
            current_token = tokens[current_token_index]
            current_token_index += 1
        else:
            raise Exception("parse_factor", "Expecting ']':")
    else:
        assignment.append(identifier)
    # EQUAL
    if current_token.m_type == TokenType.EQUAL:
        # vector
        if tokens[current_token_index].m_type == TokenType.LSBR:
            vector, current_token_index = parse_vector(tokens, current_token_index)
            assignment.append(vector)
        else:
            # expression
            expression, current_token_index = parse_expression(tokens, current_token_index)
            assignment.append(expression)
        if not identifier.m_value.lower() in symbol_table:
            symbol_table[identifier.m_value.lower()] = None
    else:
        raise Exception("parse_assignment", "Unexpected token:", tokens[current_token_index])

    return assignment, current_token_index

# tag_statement ::= TAG (EMPTY | program)+
def parse_tag_statement(tokens, current_token_index, identifier):
    if DEBUG: print(f"{COLORS['warning']}parse_tag_statement{COLORS['end']}")
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

# swap_statement ::= SWAP IDENTIFIER (LSBR expression RSBR)? IDENTIFIER (LSBR expression RSBR)?
def parse_swap_statement(tokens, current_token_index):
    if DEBUG: print(f"{COLORS['warning']}parse_swap_statement{COLORS['end']}")
    swap_statement = []
    current_token = tokens[current_token_index]
    current_token_index += 1
    # IDENTIFIER
    if current_token.m_type == TokenType.IDENTIFIER:
        identifier = current_token
        # LSBR
        if current_token_index < len(tokens) and tokens[current_token_index].m_type == TokenType.LSBR:
            current_token_index += 1
            # expression
            expression, current_token_index = parse_expression(tokens, current_token_index)
            swap_statement.append([identifier, expression])
            # RSBR
            if tokens[current_token_index].m_type == TokenType.RSBR:
                current_token_index += 1
            else:
                raise Exception("parse_swap_statement", "Unexpected token:", tokens[current_token_index])
        else:
            swap_statement.append(identifier)
    else:
        raise Exception("parse_swap_statement", "Unexpected token:", tokens[current_token_index])
    # IDENTIFIER
    current_token = tokens[current_token_index]
    current_token_index += 1
    if current_token.m_type == TokenType.IDENTIFIER:
        identifier = current_token
        # LSBR
        if current_token_index < len(tokens) and tokens[current_token_index].m_type == TokenType.LSBR:
            current_token_index += 1
            # expression
            expression, current_token_index = parse_expression(tokens, current_token_index)
            swap_statement.append([identifier, expression])
            # RSBR
            if tokens[current_token_index].m_type == TokenType.RSBR:
                current_token_index += 1
            else:
                raise Exception("parse_swap_statement", "Unexpected token:", tokens[current_token_index])
        else:
            swap_statement.append(identifier)
    else:
        raise Exception("parse_swap_statement", "Unexpected token:", tokens[current_token_index])

    return swap_statement, current_token_index

# if_statement ::= IF comparison LBRA (program)* RBRA (ELSE LBRA (program)* RBRA)?
def parse_if_statement(tokens, current_token_index):
    if DEBUG: print(f"{COLORS['warning']}parse_if_statement{COLORS['end']}")
    if_statement = []
    # comparison
    comparison, current_token_index = parse_comparison(tokens, current_token_index)
    if_statement.append(comparison)
    # LBRA
    current_token = tokens[current_token_index]
    current_token_index += 1
    if current_token.m_type == TokenType.LBRA:
        program_statements_if_condition_true = []
        # (program)*
        while current_token_index < len(tokens) and not tokens[current_token_index].m_value == RBRA:
            program, current_token_index = parse_program(tokens, current_token_index)
            program_statements_if_condition_true.append(program)
        if_statement.append(program_statements_if_condition_true)
        # RBRA
        current_token = tokens[current_token_index]
        current_token_index += 1
        if current_token.m_type == TokenType.RBRA:
            pass
        else:
            raise Exception("parse_if_statement", "Unexpected token:", tokens[current_token_index])
    else:
        raise Exception("parse_if_statement", "Unexpected token:", tokens[current_token_index])
    # (ELSE LBRA (program)* RBRA)?
    if current_token_index < len(tokens) and tokens[current_token_index].m_value == ELSE:
        # ELSE
        current_token = tokens[current_token_index]
        current_token_index += 1
        # LBRA
        current_token = tokens[current_token_index]
        current_token_index += 1
        if current_token.m_type == TokenType.LBRA:
            program_statements_if_condition_false = []
            # program
            # program, current_token_index = parse_program(tokens, current_token_index)
            # if_statement.append(program)
            # (program)*
            while current_token_index < len(tokens) and not tokens[current_token_index].m_value == RBRA:
                program, current_token_index = parse_program(tokens, current_token_index)
                # if_statement.append(program)
                program_statements_if_condition_false.append(program)
            if_statement.append(program_statements_if_condition_false)
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

# while_statement ::= WHILE comparison LBRA (program)* RBRA
def parse_while_statement(tokens, current_token_index):
    if DEBUG: print(f"{COLORS['warning']}parse_while_statement{COLORS['end']}")
    while_statement = []
    # comparison
    comparison, current_token_index = parse_comparison(tokens, current_token_index)
    while_statement.append(comparison)
    # LBRA
    current_token = tokens[current_token_index]
    current_token_index += 1
    if current_token.m_type == TokenType.LBRA:
        # (program)*
        while current_token_index < len(tokens) and not tokens[current_token_index].m_value == RBRA:
            program, current_token_index = parse_program(tokens, current_token_index)
            while_statement.append(program)
        # RBRA
        current_token = tokens[current_token_index]
        current_token_index += 1
        if current_token.m_type == TokenType.RBRA:
            pass
        else:
            raise Exception("parse_while_statement", "Unexpected token:", tokens[current_token_index], "Expected:", RBRA)
    else:
        raise Exception("parse_while_statement", "Unexpected token:", tokens[current_token_index])

    return while_statement, current_token_index

# comparison ::= expression ((EQUALS | NOT_EQUALS | LESS_THAN | GREATER_THAN) expression)*
def parse_comparison(tokens, current_token_index):
    if DEBUG: print(f"{COLORS['warning']}parse_comparison{COLORS['end']}")
    comparison = []
    # expression
    expression, current_token_index = parse_expression(tokens, current_token_index)
    comparison = expression
    # ((EQUALS | NOT_EQUALS | LESS_THAN | GREATER_THAN) expression)*
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
    if DEBUG: print(f"{COLORS['warning']}parse_expression{COLORS['end']}")
    expression = []
    # term
    term, current_token_index = parse_term(tokens, current_token_index)
    expression = term
    # ((PLUS | MINUS) term)*
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
    if DEBUG: print(f"{COLORS['warning']}parse_term{COLORS['end']}")
    term = []
    # factor
    factor, current_token_index = parse_factor(tokens, current_token_index)
    term = factor
    # ((MULTIPLY | DIVIDE) factor)*
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

# factor ::= IDENTIFIER (LSBR expression RSBR)? | BOOLEAN | INTEGER | LPAR expression RPAR
def parse_factor(tokens, current_token_index):
    if DEBUG: print(f"{COLORS['warning']}parse_factor{COLORS['end']}")
    factor = []
    current_token = tokens[current_token_index]
    current_token_index += 1
    # print(current_token)
    match current_token.m_type:
        # IDENTIFIER
        case TokenType.IDENTIFIER:
            # LSBR
            if current_token_index < len(tokens) and tokens[current_token_index].m_type == TokenType.LSBR:
                identifier = current_token
                current_token_index += 1
                # expression
                expression, current_token_index = parse_expression(tokens, current_token_index)
                factor = [identifier, expression]
                # RSBR
                current_token = tokens[current_token_index]
                current_token_index += 1
                if current_token.m_type == TokenType.RSBR:
                    pass
                else:
                    raise Exception("parse_factor", "Expecting ']'")
            else:
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
                raise Exception("parse_factor", "Expecting ')'")
        case _:
            raise Exception("parse_factor", "Unexpected token:", current_token)

    return factor, current_token_index

# vector ::= LSBR (expression (COMMA expression)*)? RSBR
def parse_vector(tokens, current_token_index):
    if DEBUG: print(f"{COLORS['warning']}parse_vector{COLORS['end']}")
    vector = []
    current_token = tokens[current_token_index]
    current_token_index += 1
    match current_token.m_type:
        # LSBR
        case TokenType.LSBR:
            # (expression (COMMA expression)*)?
            if current_token_index < len(tokens) and tokens[current_token_index].m_type != TokenType.RSBR:
                # expression
                expression, current_token_index = parse_expression(tokens, current_token_index)
                vector.append(expression)
                # (COMMA expression)*
                while current_token_index < len(tokens) and tokens[current_token_index].m_type == TokenType.COMMA:
                    current_token_index += 1
                    # expression
                    expression, current_token_index = parse_expression(tokens, current_token_index)
                    vector.append(expression)
            # RSBR
            if current_token_index < len(tokens) and tokens[current_token_index].m_type == TokenType.RSBR:
                current_token_index += 1
            else:
                raise Exception("parse_vector", "Expecting ']':")
        case _:
            raise Exception("parse_vector", "Unexpected token:", tokens[current_token_index])

    return [Token(TokenType.VECTOR), vector], current_token_index

# **** interpreter ****
def interpret(tree):
    result = ''
    node = tree
    # print(node)
    if isinstance(node, list):
        left = node[0]
        right = node[1]
    else:
        left = node
        right = None
    # print(left)
    match left.m_type:
        # ASSIGN
        case TokenType.ASSIGN:
            if isinstance(right[0], list):
                index = False
                try:
                    if isinstance(right[0][1], list):
                        index = interpret(right[0][1])
                except:
                    pass
                if index:
                    symbol_table[right[0][0].m_value]["values"][int(index)] = interpret(right[1])
                else:
                    symbol_table[right[0][0].m_value]["values"][int(symbol_table[right[0][1].m_value])] = interpret(right[1])
            else:
                symbol_table[right[0].m_value] = interpret(right[1])
        # PRINT
        case TokenType.KEYWORD if left.m_value == PRINT:
            if RUNNING_TESTS:
                STDOUT.append(interpret(right))
            else:
                print(interpret(right))
        # SWAP
        case TokenType.KEYWORD if left.m_value == SWAP:
            index_0 = False
            index_1 = False
            if isinstance(right[0], list):
                try:
                    index_0 = interpret(right[0][1])
                except:
                    pass
            if isinstance(right[1], list):
                try:
                    index_1 = interpret(right[1][1])
                except:
                    pass
            if index_0 and index_1:
                symbol_table[right[0][0].m_value]["values"][int(index_0)], symbol_table[right[1][0].m_value]["values"][int(index_1)] = symbol_table[right[1][0].m_value]["values"][int(index_1)], symbol_table[right[0][0].m_value]["values"][int(index_0)]
            elif index_0:
                symbol_table[right[0][0].m_value]["values"][int(index_0)], symbol_table[right[1].m_value] = symbol_table[right[1].m_value], symbol_table[right[0][0].m_value]["values"][int(index_0)]
            elif index_1:
                symbol_table[right[0].m_value], symbol_table[right[1][0].m_value]["values"][int(index_1)] = symbol_table[right[1][0].m_value]["values"][int(index_1)], symbol_table[right[0].m_value]
            else:
                symbol_table[right[0].m_value], symbol_table[right[1].m_value] = symbol_table[right[1].m_value], symbol_table[right[0].m_value]
        # IF
        case TokenType.KEYWORD if left.m_value == IF:
            if interpret(right[0]):
                for branch in right[1]: interpret(branch)
            else:
                try:
                    for branch in right[2]: interpret(branch)
                except:
                    pass
        # WHILE
        case TokenType.KEYWORD if left.m_value == WHILE:
            while interpret(right[0]):
                for branch in right[1:]:
                    interpret(branch)
        # TAG
        case TokenType.TAG:
            return interpret(tags_table[left.m_value])
        # identifier
        case TokenType.IDENTIFIER:
            if isinstance(symbol_table[left.m_value], dict):
                return symbol_table[left.m_value]["values"][int(interpret(right))]
            else:
                return symbol_table[left.m_value]
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
        # VECTOR
        case TokenType.VECTOR:
            return { "type": "vector", "values": [int(interpret(element)) for element in right] }
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

if (__name__ == "__main__"):
    # tests
    if "--tests" in sys.argv:
        print(f"{COLORS['cyan']}Running tests{COLORS['end']}")
        STDOUT = []
        RUNNING_TESTS = True
        # test_swap.pc
        test = "test_swap.pc"
        with open(test, "r") as file:
            STDOUT = []
            symbol_table = {}
            tags_table = {}
            tree = parse(tokenize(file.read()))
            for branch in tree: interpret(branch)
            try:
                assert STDOUT[0] == 6
                print(f"{COLORS['green']}Test case: {test} OK{COLORS['end']}")
            except:
                print(f"{COLORS['fail']}Test case: {test} Failed{COLORS['end']}")
        # test_if.pc
        test = "test_if.pc"
        with open(test, "r") as file:
            STDOUT = []
            symbol_table = {}
            tags_table = {}
            tree = parse(tokenize(file.read()))
            for branch in tree: interpret(branch)
            try:
                assert STDOUT[0] == True
                print(f"{COLORS['green']}Test case: {test} OK{COLORS['end']}")
            except:
                print(f"{COLORS['fail']}Test case: {test} Failed{COLORS['end']}")
        # test_tags.pc
        test = "test_tags.pc"
        with open(test, "r") as file:
            STDOUT = []
            symbol_table = {}
            tags_table = {}
            tree = parse(tokenize(file.read()))
            for branch in tree: interpret(branch)
            try:
                assert STDOUT[0] == 2
                print(f"{COLORS['green']}Test case: {test} OK{COLORS['end']}")
            except:
                print(f"{COLORS['fail']}Test case: {test} Failed{COLORS['end']}")
        # test_while.pc
        test = "test_while.pc"
        with open(test, "r") as file:
            STDOUT = []
            symbol_table = {}
            tags_table = {}
            tree = parse(tokenize(file.read()))
            for branch in tree: interpret(branch)
            try:
                assert STDOUT[0] == 4
                print(f"{COLORS['green']}Test case: {test} OK{COLORS['end']}")
            except:
                print(f"{COLORS['fail']}Test case: {test} Failed{COLORS['end']}")
        # test_bubblesort.pc
        test = "test_bubblesort.pc"
        with open(test, "r") as file:
            STDOUT = []
            symbol_table = {}
            tags_table = {}
            tree = parse(tokenize(file.read()))
            for branch in tree: interpret(branch)
            try:
                assert list(symbol_table["x"]["values"]) == [2, 3, 4, 5, 8]
                print(f"{COLORS['green']}Test case: {test} OK{COLORS['end']}")
            except:
                print(f"{COLORS['fail']}Test case: {test} Failed{COLORS['end']}")
        RUNNING_TESTS = False
    # load file
    elif (len(sys.argv) > 1):
        # debug
        if DEBUG: print(f"{COLORS['warning']}DEBUG{COLORS['end']}")
        file = open(sys.argv[1], "r")
        source = file.read()
        # run
        print(f"{COLORS['header']}Running {COLORS['bold']}PlayCode{COLORS['end']}{COLORS['header']} interpreter{COLORS['end']}")
        # symbol_table = {}
        tokens = tokenize(source)
        tree = parse(tokens)
        # print(tree)
        # print_tree(tree)
        for branch in tree: interpret(branch)
        # options
        if "--tokens" in sys.argv:
            for token in tokens: print(f"{COLORS['warning']}{token}{COLORS['end']}")
        if "--symbols" in sys.argv:
            print(f"{COLORS['warning']}Symbols: {symbol_table}{COLORS['end']}")
            print(f"{COLORS['warning']}Tags: {tags_table}{COLORS['end']}")
        # close
        if file: file.close()
    else:
        print(f"{COLORS['fail']}No source file provided{COLORS['end']}")
