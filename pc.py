#!/usr/local/bin python3.11

# TODO: rewrite ast visitor for lark parser output

import os
import sys

from lark import Lark

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

from src.tokenizer import *
from src.parser import *

global DEBUG
global SYMBOL_TABLE
global TAGS_TABLE

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
                    SYMBOL_TABLE[right[0][0].m_value]["values"][int(index)] = interpret(right[1])
                else:
                    SYMBOL_TABLE[right[0][0].m_value]["values"][int(SYMBOL_TABLE[right[0][1].m_value])] = interpret(right[1])
            else:
                SYMBOL_TABLE[right[0].m_value] = interpret(right[1])
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
                SYMBOL_TABLE[right[0][0].m_value]["values"][int(index_0)], SYMBOL_TABLE[right[1][0].m_value]["values"][int(index_1)] = SYMBOL_TABLE[right[1][0].m_value]["values"][int(index_1)], SYMBOL_TABLE[right[0][0].m_value]["values"][int(index_0)]
            elif index_0:
                SYMBOL_TABLE[right[0][0].m_value]["values"][int(index_0)], SYMBOL_TABLE[right[1].m_value] = SYMBOL_TABLE[right[1].m_value], SYMBOL_TABLE[right[0][0].m_value]["values"][int(index_0)]
            elif index_1:
                SYMBOL_TABLE[right[0].m_value], SYMBOL_TABLE[right[1][0].m_value]["values"][int(index_1)] = SYMBOL_TABLE[right[1][0].m_value]["values"][int(index_1)], SYMBOL_TABLE[right[0].m_value]
            else:
                SYMBOL_TABLE[right[0].m_value], SYMBOL_TABLE[right[1].m_value] = SYMBOL_TABLE[right[1].m_value], SYMBOL_TABLE[right[0].m_value]
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
            return interpret(TAGS_TABLE[left.m_value])
        # identifier
        case TokenType.IDENTIFIER:
            if isinstance(SYMBOL_TABLE[left.m_value], dict):
                return SYMBOL_TABLE[left.m_value]["values"][int(interpret(right))]
            else:
                return SYMBOL_TABLE[left.m_value]
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
    # tests : python3 pc.py --tests
    if "--tests" in sys.argv:
        print(f"{COLORS['cyan']}Running tests{COLORS['end']}")
        STDOUT = []
        RUNNING_TESTS = True
        # test_swap.pc
        test = "test_swap.pc"
        with open(test, "r") as file:
            STDOUT = []
            tree = parse(tokenize(file.read()), TAGS_TABLE)
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
            tree = parse(tokenize(file.read()), TAGS_TABLE)
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
            tree = parse(tokenize(file.read()), TAGS_TABLE)
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
            tree = parse(tokenize(file.read()), TAGS_TABLE)
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
            tree = parse(tokenize(file.read()), TAGS_TABLE)
            for branch in tree: interpret(branch)
            try:
                assert list(SYMBOL_TABLE["x"]["values"]) == [2, 3, 4, 5, 8]
                print(f"{COLORS['green']}Test case: {test} OK{COLORS['end']}")
            except:
                print(f"{COLORS['fail']}Test case: {test} Failed{COLORS['end']}")
        RUNNING_TESTS = False
    # lark
    if "--lark" in sys.argv:
        parser = Lark(open("pc.lark", "r").read(), start="program", parser='lalr')
        program = open("test_tags.pc", "r").read()
        print(parser.parse(program).pretty())
    # load file
    elif (len(sys.argv) > 1):
        # debug
        if DEBUG: print(f"{COLORS['warning']}DEBUG{COLORS['end']}")
        file = open(sys.argv[1], "r")
        # run
        print(f"{COLORS['header']}Running {COLORS['bold']}PlayCode{COLORS['end']}{COLORS['header']} interpreter{COLORS['end']}")
        tokens = tokenize(file.read())
        tree = parse(tokens, TAGS_TABLE)
        # print(tree)
        # print_tree(tree)
        for branch in tree: interpret(branch)
        # options
        if "--tokens" in sys.argv:
            for token in tokens: print(f"{COLORS['warning']}{token}{COLORS['end']}")
        if "--symbols" in sys.argv:
            print(f"{COLORS['warning']}Symbols: {SYMBOL_TABLE}{COLORS['end']}")
            print(f"{COLORS['warning']}Tags: {TAGS_TABLE}{COLORS['end']}")
        # close
        if file: file.close()
    else:
        print(f"{COLORS['fail']}No source file provided{COLORS['end']}")
