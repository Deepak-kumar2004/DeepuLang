# DeepuLang

A tiny demonstration language with English-like syntax.

## Install (editable for development)

```
pip install -e .
```

## Run a program

```
deepulang deepulang/examples/hello.dpl
```

Show version:

```
deepulang --version
```

Inspect tokens instead of executing:

```
deepulang --tokens deepulang/examples/hello.dpl
```

Inspect AST:

```
deepulang --ast deepulang/examples/hello.dpl
```

Or from source without install:

```
python3 -m deepulang deepulang/examples/hello.dpl
```

## Language Snippet

```
let greeting be "Hello, world!"
say greeting
```

## Features
- let / set variable declarations and assignments
- say for output
- if/otherwise/end
- while/do/end
- repeat <expr> times/end
- Multi-word comparators: is greater than, is not less than, etc.

## User Guide (Quick Reference)

For a fuller guide see [USER_GUIDE.md](USER_GUIDE.md). Below are the essentials.

### File Extension
Use the `.dpl` extension. Example: `hello.dpl`.

### Comments
`#` to end of line.

### Variables
Declare: `let x be 10`  Reassign: `set x to x + 1`

### Output
`say expression` prints the value followed by a newline.

### Control Flow
```
if x is greater than 5 then
	say "big"
otherwise
	say "small"
end
```

### Loops
While loop:
```
while x is greater than 0 do
	say x
	set x to x - 1
end
```
Repeat loop:
```
repeat 3 times
	say "Hi"
end
```

### Comparators (multi‑word)
```
is greater than
is less than
is equal to
is not equal to
is not greater than
is not less than
```

### Literals & Expressions
Integers (no decimals yet) and strings in double quotes supporting escapes: `\n \t \\" \\`.
Arithmetic: `+ - * /` (integer division if both operands ints).
Unary: `-x`, `not x` (logical not on truthiness).

### Newlines
End statements with a newline. Blank lines allowed.

### Minimal Program
```
let greeting be "Hello"
say greeting
```

Run it: `deepulang greeting.dpl`

## TODO
- Boolean logic (and/or)
- Decimal numbers
- Better error messages
- Standard library functions
