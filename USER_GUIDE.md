# DeepuLang User Guide

DeepuLang is a tiny educational language with readable, English-like syntax. This guide explains installation, CLI usage, syntax, and examples.

## 1. Installation

### Development (editable) install
```
pip install -e .[dev]
```
This installs the `deepulang` console script and dev tools (pytest, build, twine).

### Regular install from source directory
```
pip install .
```

### Verify
```
deepulang --version
```

## 2. Running Programs
```
deepulang path/to/program.dpl
```
Alternative without installation (from project root):
```
python3 -m deepulang path/to/program.dpl
```

### Diagnostic Modes
- Tokens: `deepulang --tokens file.dpl`
- AST: `deepulang --ast file.dpl`

## 3. File Extension
Use `.dpl` for DeepuLang source files.

## 4. Lexical Elements
- Whitespace: spaces, tabs; newlines terminate statements.
- Comments: `#` until end of line.
- Strings: double quotes, escapes: `\n`, `\t`, `\\`, `\"`.
- Numbers: integers only (no sign; unary minus applied in parsing).
- Identifiers: letters, digits, `_`, starting with letter or `_`.

## 5. Statements
```
let <ident> be <expression>
set <ident> to <expression>
say <expression>
if <condition> then <block> (otherwise <block>)? end
while <condition> do <block> end
repeat <expression> times <block> end
```
A `<block>` is one or more statements separated by newlines; `end` terminates block constructs.

## 6. Expressions
Grammar (simplified):
```
expression  := term
term        := factor ( ("+" | "-") factor )*
factor      := unary ( ("*" | "/") unary )*
unary       := ("-" | "not") unary | primary
primary     := NUMBER | STRING | IDENT | "(" expression ")"
```

## 7. Conditions and Comparators
A condition currently is a comparison of two expressions with a multi-word comparator token:
```
<expression> <comparator> <expression>
```
Comparators:
```
is greater than
is less than
is equal to
is not equal to
is not greater than
is not less than
```
Result is boolean (truthy/falsy in Python terms).

## 8. Truthiness Rules
- `0`, empty string, `None` are falsey.
- Everything else truthy.
- `not` inverts truthiness.

## 9. Variables
- Declaration: `let score be 10`
- Assignment: `set score to score + 5`
Scope is global (single environment for now).

## 10. Output
```
say <expression>
```
Prints the evaluated expression followed by newline.

## 11. Loops
### While
```
while counter is greater than 0 do
  say counter
  set counter to counter - 1
end
```
### Repeat
```
repeat 5 times
  say "tick"
end
```
Repeat count must be an integer; negative or non-integers raise runtime error.

## 12. Examples
### Countdown
```
let n be 3
while n is greater than 0 do
  say n
  set n to n - 1
end
say "Lift off!"
```
### Branching
```
let age be 20
if age is greater than 17 then
  say "adult"
otherwise
  say "minor"
end
```
### Accumulation
```
let total be 0
repeat 5 times
  set total to total + 2
end
say total  # 10
```

## 13. Error Messages
- Lexing: unexpected characters or unterminated strings raise an error with line:col.
- Parsing: unexpected tokens or missing keywords raise a ParseError with position.
- Runtime: undefined variables or invalid operations raise a RuntimeErrorDPL.

## 14. Limitations / Roadmap
- No boolean literals (`true`/`false`).
- No logical `and` / `or` chaining yet.
- Integers only (no floats).
- Single global scope.
- Minimal error recovery.

Planned improvements: boolean logic, decimals, function definitions, standard library helpers.

## 15. Contributing
See `CONTRIBUTING.md` for development workflow and release steps.

## 16. License
MIT License (see `LICENSE`).

---
Feedback and contributions welcome!
