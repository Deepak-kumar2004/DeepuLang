import deepulang
from deepulang import Lexer, Parser, Interpreter


def run_src(src: str):
    lexer = Lexer(src)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    program = parser.parse()
    interp = Interpreter()
    interp.interpret(program)
    return interp.env.values


def test_var_and_print(capsys):
    src = 'let x be 5\nsay x\n'
    env = run_src(src)
    assert env['x'] == 5
    out = capsys.readouterr().out.strip()
    assert out == '5'


def test_repeat_loop(capsys):
    src = 'let x be 0\nrepeat 3 times\n  set x to x + 1\nend\nsay x\n'
    env = run_src(src)
    assert env['x'] == 3
    out = capsys.readouterr().out.strip().splitlines()[-1]
    assert out == '3'
