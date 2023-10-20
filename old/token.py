from enum import Enum

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