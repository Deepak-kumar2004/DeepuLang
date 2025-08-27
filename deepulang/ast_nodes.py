from dataclasses import dataclass
from typing import List, Optional, Any

# AST Node definitions

class Node:
    def accept(self, visitor: "Visitor"):
        name = self.__class__.__name__
        method = getattr(visitor, f"visit_{name}")
        return method(self)

@dataclass
class Program(Node):
    statements: List[Node]

@dataclass
class VarDecl(Node):
    name: str
    expr: Node

@dataclass
class Assign(Node):
    name: str
    expr: Node

@dataclass
class Print(Node):
    expr: Node

@dataclass
class If(Node):
    condition: Node
    then_block: List[Node]
    else_block: Optional[List[Node]]

@dataclass
class While(Node):
    condition: Node
    body: List[Node]

@dataclass
class Repeat(Node):
    count_expr: Node
    body: List[Node]

@dataclass
class Comparison(Node):
    left: Node
    op: Any  # Token
    right: Node

@dataclass
class Binary(Node):
    left: Node
    op: Any  # Token
    right: Node

@dataclass
class Unary(Node):
    op: Any  # Token
    right: Node

@dataclass
class Literal(Node):
    value: Any

@dataclass
class Var(Node):
    name: str

class Visitor:
    pass
