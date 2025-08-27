"""DeepuLang - a tiny educational language.

Public API exports lexer, parser, interpreter and helper run_file().
CLI now lives in deepulang.cli providing richer options.
"""

__all__ = [
	"Lexer",
	"Parser",
	"Interpreter",
	"run_file",
	"__version__",
]

__version__ = "0.1.1"

from .lexer import Lexer  # noqa: E402
from .parser import Parser  # noqa: E402
from .interpreter import Interpreter  # noqa: E402

def run_file(path: str):
	"""Lex, parse, and interpret a .dpl source file."""
	with open(path, 'r', encoding='utf-8') as f:
		source = f.read()
	lexer = Lexer(source)
	tokens = lexer.tokenize()
	parser = Parser(tokens)
	program = parser.parse()
	interp = Interpreter()
	interp.interpret(program)

# Backwards compatibility: allow python -m deepulang
def main():  # pragma: no cover - thin wrapper
	from .cli import main as cli_main
	cli_main()

if __name__ == '__main__':  # pragma: no cover
	main()
