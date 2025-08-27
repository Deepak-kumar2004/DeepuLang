from .tokens import TokenType
from .ast_nodes import *

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def peek(self):
        return self.tokens[self.i]

    def advance(self):
        tok = self.peek()
        if tok.type != TokenType.EOF:
            self.i += 1
        return tok

    def check(self, ttype):
        return self.peek().type == ttype

    def match(self, *types):
        if self.peek().type in types:
            return self.advance()
        return None

    def consume(self, ttype, msg):
        if self.check(ttype): return self.advance()
        raise ParseError(f"{msg} at line {self.peek().line}:{self.peek().col}")

    def synchronize(self):
        # For minimal MVP just advance on error
        self.advance()

    def parse(self):
        statements = []
        while not self.check(TokenType.EOF):
            if self.check(TokenType.NEWLINE):
                self.advance(); continue
            statements.append(self.statement())
        return Program(statements)

    def statement(self):
        if self.match(TokenType.LET):
            name = self.consume(TokenType.IDENT, "Expected identifier after 'let'")
            self.consume(TokenType.BE, "Expected 'be'")
            expr = self.expression()
            return VarDecl(name.lexeme, expr)
        if self.match(TokenType.SET):
            name = self.consume(TokenType.IDENT, "Expected identifier after 'set'")
            self.consume(TokenType.TO, "Expected 'to'")
            expr = self.expression()
            return Assign(name.lexeme, expr)
        if self.match(TokenType.SAY):
            return Print(self.expression())
        if self.match(TokenType.IF):
            cond = self.condition()
            self.consume(TokenType.THEN, "Expected 'then'")
            then_block = self.block()
            else_block = None
            if self.match(TokenType.OTHERWISE):
                else_block = self.block()
            self.consume(TokenType.END, "Expected 'end'")
            return If(cond, then_block, else_block)
        if self.match(TokenType.WHILE):
            cond = self.condition()
            self.consume(TokenType.DO, "Expected 'do'")
            body = self.block()
            self.consume(TokenType.END, "Expected 'end'")
            return While(cond, body)
        if self.match(TokenType.REPEAT):
            count_expr = self.expression()
            self.consume(TokenType.TIMES, "Expected 'times'")
            body = self.block()
            self.consume(TokenType.END, "Expected 'end'")
            return Repeat(count_expr, body)
        raise ParseError(f"Unexpected token {self.peek()}")

    def block(self):
        # Accept optional NEWLINE
        if self.match(TokenType.NEWLINE):
            pass
        statements = []
        while (not self.check(TokenType.END) and
               not self.check(TokenType.OTHERWISE) and
               not self.check(TokenType.EOF)):
            if self.check(TokenType.NEWLINE):
                self.advance()
                continue
            statements.append(self.statement())
            if self.check(TokenType.NEWLINE):
                self.advance()
        return statements

    def condition(self):
        # For MVP just a comparison (extend later)
        left = self.expression()
        comp_token = self.match(TokenType.IS_GT, TokenType.IS_LT, TokenType.IS_EQ,
                                TokenType.IS_NE, TokenType.IS_NOT_GT, TokenType.IS_NOT_LT)
        if not comp_token:
            raise ParseError("Expected comparator in condition")
        right = self.expression()
        return Comparison(left, comp_token, right)

    def expression(self):
        return self.term()

    def term(self):
        expr = self.factor()
        while True:
            op = self.match(TokenType.PLUS, TokenType.MINUS)
            if not op: break
            right = self.factor()
            expr = Binary(expr, op, right)
        return expr

    def factor(self):
        expr = self.unary()
        while True:
            op = self.match(TokenType.STAR, TokenType.SLASH)
            if not op: break
            right = self.unary()
            expr = Binary(expr, op, right)
        return expr

    def unary(self):
        op = self.match(TokenType.MINUS, TokenType.NOT)
        if op:
            right = self.unary()
            return Unary(op, right)
        return self.primary()

    def primary(self):
        tok = self.peek()
        if tok.type == TokenType.NUMBER:
            self.advance()
            return Literal(tok.value)
        if tok.type == TokenType.STRING:
            self.advance()
            return Literal(tok.value)
        if tok.type == TokenType.IDENT:
            self.advance()
            return Var(tok.lexeme)
        if tok.type == TokenType.LPAREN:
            self.advance()
            expr = self.expression()
            self.consume(TokenType.RPAREN, "Expected ')'")
            return expr
        raise ParseError(f"Unexpected token in expression {tok}")