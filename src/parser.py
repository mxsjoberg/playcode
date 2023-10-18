from src.consts import *
from src.token import *

SYMBOL_TABLE = {}
TAGS_TABLE = {}

# **** parser ****
def parse(tokens, TAGS_TABLE):
    TAGS_TABLE = TAGS_TABLE
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
        if not identifier.m_value.lower() in SYMBOL_TABLE:
            SYMBOL_TABLE[identifier.m_value.lower()] = None
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
        TAGS_TABLE[identifier.m_value] = program

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
