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
