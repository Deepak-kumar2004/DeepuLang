from .tokens import TokenType
from .ast_nodes import *

class RuntimeErrorDPL(Exception):
    pass

class Environment:
    def __init__(self):
        self.values = {}
    def define(self, name, value):
        self.values[name] = value
    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
        else:
            raise RuntimeErrorDPL(f"Undefined variable '{name}'")
    def get(self, name):
        if name in self.values:
            return self.values[name]
        raise RuntimeErrorDPL(f"Undefined variable '{name}'")

class Interpreter(Visitor):
    def __init__(self):
        self.env = Environment()

    def interpret(self, program: Program):
        for stmt in program.statements:
            self.execute(stmt)

    # Visitor methods
    def execute(self, node):
        return node.accept(self)

    def visit_Program(self, node: Program):
        self.interpret(node)

    def visit_VarDecl(self, node: VarDecl):
        value = self.evaluate(node.expr)
        self.env.define(node.name, value)

    def visit_Assign(self, node: Assign):
        value = self.evaluate(node.expr)
        self.env.assign(node.name, value)

    def visit_Print(self, node: Print):
        value = self.evaluate(node.expr)
        print(value)

    def visit_If(self, node: If):
        if self.is_truthy(self.evaluate(node.condition)):
            self.execute_block(node.then_block)
        elif node.else_block is not None:
            self.execute_block(node.else_block)

    def visit_While(self, node: While):
        while self.is_truthy(self.evaluate(node.condition)):
            self.execute_block(node.body)

    def visit_Repeat(self, node: Repeat):
        count = self.evaluate(node.count_expr)
        if not isinstance(count, int):
            raise RuntimeErrorDPL("Repeat count must be integer")
        for _ in range(count):
            self.execute_block(node.body)

    def visit_Comparison(self, node: Comparison):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        t = node.op.type
        if t == TokenType.IS_GT:
            return left > right
        if t == TokenType.IS_LT:
            return left < right
        if t == TokenType.IS_EQ:
            return left == right
        if t == TokenType.IS_NE:
            return left != right
        if t == TokenType.IS_NOT_GT:
            return not (left > right)
        if t == TokenType.IS_NOT_LT:
            return not (left < right)
        raise RuntimeErrorDPL(f"Unknown comparator {t}")

    def visit_Binary(self, node: Binary):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        t = node.op.type
        if t == TokenType.PLUS:
            return left + right
        if t == TokenType.MINUS:
            return left - right
        if t == TokenType.STAR:
            return left * right
        if t == TokenType.SLASH:
            return left // right if isinstance(left, int) and isinstance(right, int) else left / right
        raise RuntimeErrorDPL(f"Unknown binary operator {t}")

    def visit_Unary(self, node: Unary):
        right = self.evaluate(node.right)
        t = node.op.type
        if t == TokenType.MINUS:
            return -right
        if t == TokenType.NOT:
            return not self.is_truthy(right)
        raise RuntimeErrorDPL(f"Unknown unary operator {t}")

    def visit_Literal(self, node: Literal):
        return node.value

    def visit_Var(self, node: Var):
        return self.env.get(node.name)

    # Helpers
    def evaluate(self, node):
        return node.accept(self)

    def is_truthy(self, value):
        if value is None: return False
        if isinstance(value, bool): return value
        return bool(value)

    def execute_block(self, stmts):
        for s in stmts:
            self.execute(s)
