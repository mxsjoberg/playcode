# $ python lark_driver.py

from lark import Lark

grammar = open("pc.lark", "r").read()

parser = Lark(grammar, start="program", parser='lalr')

program = open("test_tags.pc", "r").read()

print(parser.parse(program).pretty())