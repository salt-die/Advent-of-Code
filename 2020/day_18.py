"""Also see shunting_yard.py for an alternative method of solving."""
from itertools import tee

import aoc_helper
from more_itertools import unzip
from sly import Lexer, Parser


class MathLexer(Lexer):
    tokens = {NUMBER}
    ignore = ' '
    literals = {'+', '*', '(', ')'}

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t


class MathParser(Parser):
    tokens = MathLexer.tokens

    precedence = (
        ('left', '+', '*'),
        ('left', '(', ')'),
    )

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

lexer = MathLexer()
raw = aoc_helper.day(18)
tokens_a, tokens_b = unzip(tee(lexer.tokenize(line)) for line in raw.splitlines())

def part_one():
    parser = MathParser()
    return sum(map(parser.parse, tokens_a))

def part_two():
    # Patch parser and rebuild
    MathParser.precedence = (
        ('left', '*'),
        ('left', '+'),
        ('left', '(', ')'),
    )
    MathParser._build(MathParser.__dict__.items())

    parser = MathParser()
    return sum(map(parser.parse, tokens_b))

aoc_helper.submit(18, part_one)
aoc_helper.submit(18, part_two)
