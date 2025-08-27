import argparse
import sys
from pathlib import Path
from . import __version__, run_file, Lexer, Parser, Interpreter


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="deepulang",
        description="DeepuLang - tiny educational language"
    )
    parser.add_argument("source", nargs="?", help="Path to .dpl source file")
    parser.add_argument("--version", action="store_true", help="Show version and exit")
    parser.add_argument("--tokens", action="store_true", help="Print tokens instead of executing")
    parser.add_argument("--ast", action="store_true", help="Print parsed AST (repr) and exit")
    args = parser.parse_args(argv)

    if args.version:
        print(f"deepulang {__version__}")
        return 0

    if not args.source:
        parser.print_usage()
        print("error: missing source file")
        return 1

    path = Path(args.source)
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 1

    with open(path, 'r', encoding='utf-8') as f:
        source = f.read()

    lexer = Lexer(source)
    tokens = lexer.tokenize()

    if args.tokens:
        for t in tokens:
            print(t)
        return 0

    parser_obj = Parser(tokens)
    program = parser_obj.parse()

    if args.ast:
        print(program)
        return 0

    interp = Interpreter()
    interp.interpret(program)
    return 0

if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
