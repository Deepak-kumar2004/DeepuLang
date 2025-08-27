from enum import Enum, auto

class TokenType(Enum):
    # Single char
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    LPAREN = auto()
    RPAREN = auto()
    NEWLINE = auto()
    EOF = auto()

    # Literals
    NUMBER = auto()
    STRING = auto()
    IDENT = auto()

    # Keywords
    LET = auto()
    BE = auto()
    SET = auto()
    TO = auto()
    IF = auto()
    THEN = auto()
    OTHERWISE = auto()
    END = auto()
    WHILE = auto()
    DO = auto()
    REPEAT = auto()
    TIMES = auto()
    SAY = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    # Comparators (multiword normalized)
    IS_GT = auto()
    IS_LT = auto()
    IS_EQ = auto()
    IS_NE = auto()
    IS_NOT_GT = auto()
    IS_NOT_LT = auto()

KEYWORDS = {
    "let": TokenType.LET,
    "be": TokenType.BE,
    "set": TokenType.SET,
    "to": TokenType.TO,
    "if": TokenType.IF,
    "then": TokenType.THEN,
    "otherwise": TokenType.OTHERWISE,
    "end": TokenType.END,
    "while": TokenType.WHILE,
    "do": TokenType.DO,
    "repeat": TokenType.REPEAT,
    "times": TokenType.TIMES,
    "say": TokenType.SAY,
    "and": TokenType.AND,
    "or": TokenType.OR,
    "not": TokenType.NOT,
}

MULTIWORD_COMPARATORS = [
    ("is not greater than", TokenType.IS_NOT_GT),
    ("is not less than", TokenType.IS_NOT_LT),
    ("is not equal to", TokenType.IS_NE),
    ("is greater than", TokenType.IS_GT),
    ("is less than", TokenType.IS_LT),
    ("is equal to", TokenType.IS_EQ),
    ("is not equal to", TokenType.IS_NE),  # duplicate pattern alternative
]

class Token:
    def __init__(self, type_, lexeme, value, line, col):
        self.type = type_
        self.lexeme = lexeme
        self.value = value
        self.line = line
        self.col = col
    def __repr__(self):
        return f"Token({self.type}, {self.lexeme}, {self.value}, {self.line}:{self.col})"