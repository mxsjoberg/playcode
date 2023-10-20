#!/usr/local/bin python3.11

import os
import sys

from lark import Lark, Tree, Transformer

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

parser = Lark(open("pc.lark", "r").read(), start="program", parser="lalr")

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
                    TAG_TABLE[tree.children[0].value] = tree.children[1]
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
        case "assert_stmt":
            value = str(visitor(tree.children[0]))
            if not value == tree.children[1].children[0][1:-1]:
                print(f"Assert error: {value} not equal to {tree.children[1].children[0][1:-1]}")
        case "print_stmt":
            output = str(visitor(tree.children[0]))
            if len(tree.children) > 1 and tree.children[1].data == "assert":
                if not output == tree.children[1].children[0][1:-1]:
                    STDERR.append(f"Assert error: {output} not equal to {tree.children[1].children[0][1:-1]}")
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
        case "true":
            return True
        case "false":
            return False

# **** main ****
if (__name__ == "__main__"):
    # python3 pc.py --tests
    if "--tests" in sys.argv:
        print(f"{COLORS['cyan']}Running tests{COLORS['end']}")
        for path, subdirs, files in os.walk("tests"):
            for name in files:
                test = os.path.join(path, name)
                tree = parser.parse(open(test, "r").read())
                SYMBOL_TABLE = {}
                TAG_TABLE = {}
                STDOUT = []
                STDERR = []
                for branch in tree.children: visitor(branch)
                if len(STDERR) == 0:
                    print(f"  {test} {COLORS['green']}OK{COLORS['end']}")
                else:
                    print(f"  {test} {COLORS['fail']}Failed{COLORS['end']}")
                    for error in enumerate(STDERR, 1):
                        print(f"    {COLORS['fail']}{error[0]} - {error[1]}{COLORS['end']}")
        print(f"{COLORS['cyan']}Done{COLORS['end']}")
    # python3 pc.py <file> --tables
    elif len(sys.argv) > 1:
        file = open(sys.argv[1], "r").read()
        tree = parser.parse(file)
        SYMBOL_TABLE = {}
        TAG_TABLE = {}
        STDOUT = []
        STDERR = []
        for branch in tree.children: visitor(branch)
        if not len(STDOUT) == 0:
            for output in STDOUT: print(output)
        if "--tables" in sys.argv:
            print(f"{COLORS['warning']}SYMBOL_TABLE: {SYMBOL_TABLE}{COLORS['end']}")
            print(f"{COLORS['warning']}TAG_TABLE: {TAG_TABLE}{COLORS['end']}")
    else:
        print(f"{COLORS['fail']}No source file provided{COLORS['end']}")
