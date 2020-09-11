#!/usr/bin/env python3
import re
import sys

class Syntax:
    def __init__(self, string=""):
        self.string = string

class Preprocessor(Syntax):
    match = r"(#)\s*(include)\s*(<.*?>)"
    name = "Preprocessor directives"
    length = len(name) + 2

class Type(Syntax):
    match = r"(int|char\*\*|uint_fast64_t|char\*|char\[\])"
    name = "Types"
    length = len(name) + 2

class Variable(Syntax):
    match = r"(\w+)"
    name = "Variables"
    length = len(name) + 2

class Operator(Syntax):
    match = r"(,|\+\+|--|\+=|<=|>=|/=|&&|&=|\+|-|\*|/|%|>>|<<|>|<|&|~|=)"
    name = "Operators"
    length = len(name) + 2

class Number(Syntax):
    match = r"(\d+)"
    name = "Numbers"
    length = len(name) + 2

class Keyword(Syntax):
    match = r"(if|for|return|while)"
    name = "Keywords"
    length = len(name) + 2

class Function(Syntax):
    match = r"(main|malloc|memset|strtoumax|sqrt|puts|log10|putchar|free)"
    name = "Functions"
    length = len(name) + 2

class Bracket(Syntax):
    match = r"(\[|\])"
    name = "Square brackets"
    length = len(name) + 2

class Parenthese(Syntax):
    match = r"(\(|\))"
    name = "Parentheses"
    length = len(name) + 2

class Brace(Syntax):
    match = r"(\{|\})"
    name = "Curly braces"
    length = len(name) + 2

class Semicolon(Syntax):
    match = r"(;)"
    name = "Semicolons"
    length = len(name) + 2

class NoMatch(Syntax):
    match = r"."
    name = "No match"


def center(string, length):
    diff = length - len(string)
    if diff < 0:
        sys.exit("error")
    f = diff // 2
    r = diff - f
    return ' ' * f + string + ' ' * r

contents = re.sub(r"/\*.*?\*/", "", sys.stdin.read(), flags=re.DOTALL)
l = []
while contents != "":
    for c in [Preprocessor, Type, Keyword, Function, Number, Bracket, Parenthese, Brace, Semicolon, Operator, Variable, NoMatch]:
        m = re.search(r"^\s*" + c.match, contents, re.DOTALL)
        if m:
            l.append(c(''.join(m.groups())))
            contents = contents[m.end():]
            break

l = [m for m in l if not isinstance(m, NoMatch)]

order = [Type, Variable, Operator, Number, Keyword, Function, Bracket, Parenthese, Brace, Semicolon, Preprocessor]

output = "/*"
for s in order:
    s.length = max(s.length, max([len(m.string) + 6 for m in l if isinstance(m, s)]))
    output += "|" + center(s.name, s.length)
output += "|*/\n/*"

pos = 0
for m in l:
    while not isinstance(m, order[pos]):
        output += "|*/" + ' ' * (order[pos].length-4) + "/*"
        pos += 1
        if pos == len(order):
            output += "|*/\n/*"
            pos = 0
    output += "|*/" + center(m.string, order[pos].length-4) + "/*"
    pos += 1
    if pos == len(order):
        output += "|*/\n/*"
        pos = 0

while pos < len(order):
    output += "|*/" + ' ' * (order[pos].length-4) + "/*"
    pos += 1

output += "|*/"
print(output)
