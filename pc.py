#!/usr/local/bin python3.11

import os
import sys

from lark import Lark, Tree, Transformer

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

def visitor(tree):
    # print(tree.data)
    match tree.data:
        case "program":
            for branch in tree.children:
                visitor(branch)
            return
        case "taggable":
            try:
                if tree.children[0].type == "TAG":
                    TAG_TABLE[tree.children[0]] = tree.children[1]
            except:
                return visitor(tree.children[0])
        case "assign_stmt":
            # TODO: left.children[0].value for CNAME? is this best way?
            left, right = tree.children
            SYMBOL_TABLE[left.children[0].value] = visitor(right)
        case "tag_stmt":
            return visitor(TAG_TABLE[tree.children[0].value])
        case "swap_stmt":
            left, right = tree.children
            if len(left.children) > 1 and len(right.children) > 1:
                tmp = SYMBOL_TABLE[left.children[0]][visitor(left.children[1])]
                SYMBOL_TABLE[left.children[0]][visitor(left.children[1])] = SYMBOL_TABLE[right.children[0]][visitor(right.children[1])]
                SYMBOL_TABLE[right.children[0]][visitor(right.children[1])] = tmp
            elif len(left.children) > 1:
                tmp = SYMBOL_TABLE[left.children[0]][visitor(left.children[1])]
                SYMBOL_TABLE[left.children[0]][visitor(left.children[1])] = SYMBOL_TABLE[right.children[0]]
                SYMBOL_TABLE[right.children[0]] = tmp
            elif len(right.children) > 1:
                tmp = SYMBOL_TABLE[left.children[0]]
                SYMBOL_TABLE[left.children[0]] = SYMBOL_TABLE[right.children[0]][visitor(right.children[1])]
                SYMBOL_TABLE[right.children[0]][visitor(right.children[1])] = tmp
            else:
                tmp = SYMBOL_TABLE[left.children[0]]
                SYMBOL_TABLE[left.children[0]] = SYMBOL_TABLE[right.children[0]]
                SYMBOL_TABLE[right.children[0]] = tmp
        case "if_stmt":
            if bool(visitor(tree.children[0])):
                return visitor(tree.children[1])
            elif len(tree.children) > 2:
                return visitor(tree.children[2])
        case "while_stmt":
            while visitor(tree.children[0]):
                visitor(tree.children[1])
        case "print_stmt":
            output = str(visitor(tree.children[0]))
            if len(tree.children) > 1 and tree.children[1].data == "assert":
                if not output == tree.children[1].children[0][1:-1]:
                    print(f"Assert error: {output} not equal to {tree.children[1].children[0][1:-1]}")
            STDOUT.append(output)
        case "comparison":
            return visitor(tree.children[0])
        case "expr":
            return visitor(tree.children[0])
        case "term":
            return visitor(tree.children[0])
        case "factor":
            return visitor(tree.children[0])
        case "add":
            left, right = tree.children
            return int(visitor(left)) + int(visitor(right))
        case "sub":
            left, right = tree.children
            return int(visitor(left)) - int(visitor(right))
        case "mul":
            left, right = tree.children
            return int(visitor(left)) * int(visitor(right))
        case "div":
            left, right = tree.children
            return int(visitor(left)) / int(visitor(right))
        case "eq":
            left, right = tree.children
            return int(visitor(left)) == int(visitor(right))
        case "neq":
            left, right = tree.children
            return int(visitor(left)) != int(visitor(right))
        case "lt":
            left, right = tree.children
            return int(visitor(left)) < int(visitor(right))
        case "gt":
            left, right = tree.children
            return int(visitor(left)) > int(visitor(right))
        case "vector":
            data = []
            for branch in tree.children:
                data.append(visitor(branch))
            return list(data)
        case "number":
            return int(tree.children[0])
        case "identifier":
            if len(tree.children) > 1:
                return SYMBOL_TABLE[str(tree.children[0])][int(visitor(tree.children[1]))]
            else:
                return SYMBOL_TABLE[str(tree.children[0])]
        case "assert":
            print("-- HERE 1")
            pass
        case "true":
            return True
        case "false":
            return False

# **** main ****
if (__name__ == "__main__"):
    # python3 pc.py --tests
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
    # python3 pc.py --lark
    if "--lark" in sys.argv:
        parser = Lark(open("pc.lark", "r").read(), start="program", parser="lalr")
        tree = parser.parse(open("test.pc", "r").read())
        # print(tree)
        SYMBOL_TABLE = {}
        TAG_TABLE = {}
        STDOUT = []
        for branch in tree.children: visitor(branch)
        print(SYMBOL_TABLE)
        print(STDOUT)
    # python3 pc.py <file>
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
