import re
from .tokens import Token, TokenType, KEYWORDS, MULTIWORD_COMPARATORS

class LexError(Exception):
    pass

class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1
        self.length = len(source)

    def peek(self, n=0):
        idx = self.pos + n
        return self.source[idx] if idx < self.length else '\0'

    def advance(self):
        ch = self.peek()
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def match(self, expected):
        if self.peek() == expected:
            self.advance()
            return True
        return False

    def skip_ws_and_comments(self):
        while True:
            ch = self.peek()
            if ch in ' \t\r':
                self.advance()
                continue
            if ch == '#':
                while self.peek() not in ('\n', '\0'):
                    self.advance()
                continue
            break

    def try_multiword_comparator(self):
        # Look ahead up to longest phrase length
        remaining = self.source[self.pos:].lower()
        for phrase, ttype in MULTIWORD_COMPARATORS:
            if remaining.startswith(phrase):
                # Ensure word boundary
                end_idx = len(phrase)
                if end_idx == len(remaining) or not remaining[end_idx].isalpha():
                    # consume phrase
                    for _ in range(len(phrase)):
                        self.advance()
                    return Token(ttype, phrase, None, self.line, self.col)
        return None

    def string(self):
        start_line, start_col = self.line, self.col
        value = ""
        while True:
            ch = self.advance()
            if ch == '\0':
                raise LexError(f"Unterminated string at {start_line}:{start_col}")
            if ch == '"':
                break
            if ch == '\\':
                nxt = self.advance()
                escapes = {'n':'\n','t':'\t','"':'"','\\':'\\'}
                value += escapes.get(nxt, nxt)
            else:
                value += ch
        return Token(TokenType.STRING, value, value, start_line, start_col)

    def number(self):
        start_line, start_col = self.line, self.col
        num = ""
        while self.peek().isdigit():
            num += self.advance()
        # (Optional: handle decimals)
        return Token(TokenType.NUMBER, num, int(num), start_line, start_col)

    def identifier(self):
        start_line, start_col = self.line, self.col
        ident = ""
        while self.peek().isalnum() or self.peek() == '_':
            ident += self.advance()
        lower = ident.lower()
        ttype = KEYWORDS.get(lower)
        if ttype:
            return Token(ttype, ident, lower, start_line, start_col)
        return Token(TokenType.IDENT, ident, ident, start_line, start_col)

    def tokenize(self):
        tokens = []
        while True:
            self.skip_ws_and_comments()
            ch = self.peek()
            if ch == '\0':
                tokens.append(Token(TokenType.EOF, "", None, self.line, self.col))
                break

            # NEWLINE
            if ch == '\n':
                self.advance()
                tokens.append(Token(TokenType.NEWLINE, '\\n', None, self.line, self.col))
                continue

            # Multiword comparator attempt (only when starting with 'i' maybe)
            if ch.lower() == 'i':
                comp = self.try_multiword_comparator()
                if comp:
                    tokens.append(comp)
                    continue

            if ch == '"':
                self.advance()  # consume opening quote
                tokens.append(self.string())
                continue
            if ch.isdigit():
                tokens.append(self.number())
                continue
            if ch.isalpha() or ch == '_':
                tokens.append(self.identifier())
                continue

            # Single-character tokens
            start_line, start_col = self.line, self.col
            if ch == '+':
                self.advance(); tokens.append(Token(TokenType.PLUS, '+', None, start_line, start_col)); continue
            if ch == '-':
                self.advance(); tokens.append(Token(TokenType.MINUS, '-', None, start_line, start_col)); continue
            if ch == '*':
                self.advance(); tokens.append(Token(TokenType.STAR, '*', None, start_line, start_col)); continue
            if ch == '/':
                self.advance(); tokens.append(Token(TokenType.SLASH, '/', None, start_line, start_col)); continue
            if ch == '(':
                self.advance(); tokens.append(Token(TokenType.LPAREN, '(', None, start_line, start_col)); continue
            if ch == ')':
                self.advance(); tokens.append(Token(TokenType.RPAREN, ')', None, start_line, start_col)); continue

            raise LexError(f"Unexpected character '{ch}' at {self.line}:{self.col}")
        return tokens