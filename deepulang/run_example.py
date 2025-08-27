"""Run the hello.dpl example through the lexer and print tokens.

Invocation:
        python3 -m deepulang.run_example
or
        python3 deepulang/run_example.py

The first form ensures proper package-relative imports. The second adds
the parent directory of this file to sys.path to allow relative import usage.
"""

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
                # Executed as a script: add parent directory so 'deepulang' is a package
                pkg_root = Path(__file__).resolve().parent
                sys.path.append(str(pkg_root.parent))

from .lexer import Lexer  # type: ignore
from .tokens import TokenType  # noqa: F401  (imported for potential future use)

example_path = Path(__file__).resolve().parent / "examples" / "hello.dpl"
with open(example_path, "r", encoding="utf-8") as f:
        source = f.read()

lexer = Lexer(source)
tokens = lexer.tokenize()
for t in tokens:
        print(t)
