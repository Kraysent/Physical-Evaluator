from __future__ import division

import math
import re

import py_expression_eval.standart_functions as funcs
from py_expression_eval.expression import Expression
from py_expression_eval.token import *


def substitute(self, variable, expr):
    if not isinstance(expr, Expression):
        expr = Parser().parse(str(expr))

    newexpression = []

    for i in range(0, len(self.tokens)):
        item = self.tokens[i]
        type_ = item.type_
        if type_ == TVAR and item.index_ == variable:
            for j in range(0, len(expr.tokens)):
                expritem = expr.tokens[j]
                replitem = Token(
                    expritem.type_,
                    expritem.index_,
                    expritem.prio_,
                    expritem.number_,
                )
                newexpression.append(replitem)
        else:
            newexpression.append(item)

    ret = Expression(newexpression, self.ops1, self.ops2, self.functions)
    
    return ret

Expression.subtitute = substitute

class Parser:
    PRIMARY      = 1
    OPERATOR     = 2
    FUNCTION     = 4
    LPAREN       = 8
    RPAREN       = 16
    COMMA        = 32
    SIGN         = 64
    CALL         = 128
    NULLARY_CALL = 256


    def __init__(self, string_literal_quotes = ("'", "\"")):
        self.string_literal_quotes = string_literal_quotes

        self.success = False
        self.errormsg = ''
        self.expression = ''

        self.pos = 0

        self.tokennumber = 0
        self.tokenprio = 0
        self.tokenindex = 0
        self.tmpprio = 0

        self.ops1 = funcs.unary_functions

        self.ops2 = funcs.binary_functions

        self.functions = {
            'random': funcs.random,
            'fac': funcs.fac,
            'log': funcs.log,
            'min': funcs.min,
            'max': funcs.max,
            'pyt': funcs.pyt,
            'pow': funcs.pow,
            'atan2': funcs.atan2,
            'concat': funcs.concat,
            'if': funcs.if_function
        }

        self.consts = {
            'E': math.e,
            'PI': math.pi,
        }

    def parse(self, expr):
        self.errormsg = ''
        self.success = True
        operstack = []
        tokenstack = []
        self.tmpprio = 0
        expected = self.PRIMARY | self.LPAREN | self.FUNCTION | self.SIGN
        noperators = 0
        self.expression = expr
        self.pos = 0

        while self.pos < len(self.expression):
            if self.is_operator():
                if self.is_sign() and expected & self.SIGN:
                    if self.is_negative_sign():
                        self.tokenprio = 5
                        self.tokenindex = '-'
                        noperators += 1
                        self.add_func(tokenstack, operstack, TOP1)

                    expected = self.PRIMARY | self.LPAREN | self.FUNCTION | self.SIGN
                elif self.is_logical_not() and expected & self.SIGN:
                    self.tokenprio = 2
                    self.tokenindex = 'not'
                    noperators += 1
                    self.add_func(tokenstack, operstack, TOP1)
                    expected = self.PRIMARY | self.LPAREN | self.FUNCTION | self.SIGN
                elif self.is_comment():
                    pass
                else:
                    if expected and self.OPERATOR == 0:
                        self.error_parsing(self.pos, 'unexpected operator')

                    noperators += 2
                    self.add_func(tokenstack, operstack, TOP2)
                    expected = self.PRIMARY | self.LPAREN | self.FUNCTION | self.SIGN
            elif self.is_number():
                if expected and self.PRIMARY == 0:
                    self.error_parsing(self.pos, 'unexpected number')

                token = Token(TNUMBER, 0, 0, self.tokennumber)
                tokenstack.append(token)
                expected = self.OPERATOR | self.RPAREN | self.COMMA
            elif self.is_string():
                if (expected & self.PRIMARY) == 0:
                    self.error_parsing(self.pos, 'unexpected string')

                token = Token(TNUMBER, 0, 0, self.tokennumber)
                tokenstack.append(token)
                expected = self.OPERATOR | self.RPAREN | self.COMMA
            elif self.is_left_parenth():
                if (expected & self.LPAREN) == 0:
                    self.error_parsing(self.pos, 'unexpected \"(\"')

                if expected & self.CALL:
                    noperators += 2
                    self.tokenprio = -2
                    self.tokenindex = -1
                    self.add_func(tokenstack, operstack, TFUNCALL)

                expected = self.PRIMARY | self.LPAREN | self.FUNCTION | self.SIGN | self.NULLARY_CALL
            elif self.is_right_parenth():
                if expected & self.NULLARY_CALL:
                    token = Token(TNUMBER, 0, 0, [])
                    tokenstack.append(token)
                elif (expected & self.RPAREN) == 0:
                    self.error_parsing(self.pos, 'unexpected \")\"')

                expected = self.OPERATOR | self.RPAREN | self.COMMA | self.LPAREN | self.CALL
            elif self.is_comma():
                if (expected & self.COMMA) == 0:
                    self.error_parsing(self.pos, 'unexpected \",\"')

                self.add_func(tokenstack, operstack, TOP2)
                noperators += 2
                expected = self.PRIMARY | self.LPAREN | self.FUNCTION | self.SIGN
            elif self.is_const():
                if (expected & self.PRIMARY) == 0:
                    self.error_parsing(self.pos, 'unexpected constant')

                consttoken = Token(TNUMBER, 0, 0, self.tokennumber)
                tokenstack.append(consttoken)
                expected = self.OPERATOR | self.RPAREN | self.COMMA
            elif self.is_binary_operator():
                if (expected & self.FUNCTION) == 0:
                    self.error_parsing(self.pos, 'unexpected function')

                self.add_func(tokenstack, operstack, TOP2)
                noperators += 2
                expected = self.LPAREN
            elif self.is_unary_operator():
                if (expected & self.FUNCTION) == 0:
                    self.error_parsing(self.pos, 'unexpected function')

                self.add_func(tokenstack, operstack, TOP1)
                noperators += 1
                expected = self.LPAREN
            elif self.is_var():
                if (expected & self.PRIMARY) == 0:
                    self.error_parsing(self.pos, 'unexpected variable')

                vartoken = Token(TVAR, self.tokenindex, 0, 0)
                tokenstack.append(vartoken)
                expected = self.OPERATOR | self.RPAREN | self.COMMA | self.LPAREN | self.CALL
            elif self.is_white():
                pass
            else:
                if self.errormsg == '':
                    self.error_parsing(self.pos, 'unknown character')
                else:
                    self.error_parsing(self.pos, self.errormsg)
        if self.tmpprio < 0 or self.tmpprio >= 10:
            self.error_parsing(self.pos, 'unmatched \"()\"')
        while len(operstack) > 0:
            tmp = operstack.pop()
            tokenstack.append(tmp)
        if (noperators + 1) != len(tokenstack):
            self.error_parsing(self.pos, 'parity')

        return Expression(tokenstack, self.ops1, self.ops2, self.functions)

    def evaluate(self, expr, variables):
        return self.parse(expr).evaluate(variables)

    def error_parsing(self, column, msg):
        self.success = False
        self.errormsg = 'parse error [column ' + str(column) + ']: ' + msg + ', expression: ' + self.expression

        raise Exception(self.errormsg)

    def add_func(self, tokenstack, operstack, type_):
        operator = Token(
            type_,
            self.tokenindex,
            self.tokenprio + self.tmpprio,
            0,
        )
        while len(operstack) > 0:
            if operator.prio_ <= operstack[len(operstack) - 1].prio_:
                tokenstack.append(operstack.pop())
            else:
                break

        operstack.append(operator)

    def is_number(self):
        r = False

        if self.expression[self.pos] == 'E':
            return False

        # number in scientific notation
        pattern = r'([-+]?([0-9]*\.?[0-9]*)[eE][-+]?[0-9]+).*'
        match = re.match(pattern, self.expression[self.pos: ])
        if match:
            self.pos += len(match.group(1))
            self.tokennumber = float(match.group(1))

            return True

        # number in decimal
        str = ''
        while self.pos < len(self.expression):
            code = self.expression[self.pos]
            if (code >= '0' and code <= '9') or code == '.':
                if (len(str) == 0 and code == '.' ):
                    str = '0'
                str += code
                self.pos += 1
                try:
                    self.tokennumber = int(str)
                except ValueError:
                    self.tokennumber = float(str)
                r = True
            else:
                break
        return r

    def unescape(self, v, pos):
        buffer = []
        escaping = False

        for i in range(0, len(v)):
            c = v[i]

            if escaping:
                if c == "'":
                    buffer.append("'")
                    break
                elif c == '\\':
                    buffer.append('\\')
                    break
                elif c == '/':
                    buffer.append('/')
                    break
                elif c == 'b':
                    buffer.append('\b')
                    break
                elif c == 'f':
                    buffer.append('\f')
                    break
                elif c == 'n':
                    buffer.append('\n')
                    break
                elif c == 'r':
                    buffer.append('\r')
                    break
                elif c == 't':
                    buffer.append('\t')
                    break
                elif c == 'u':
                    # interpret the following 4 characters
                    # as the hex of the unicode code point
                    codePoint = int(v[i + 1, i + 5], 16)
                    buffer.append(unichr(codePoint))
                    i += 4
                    break
                else:
                    raise self.error_parsing(
                        pos + i,
                        'Illegal escape sequence: \'\\' + c + '\'',
                    )
                escaping = False
            else:
                if c == '\\':
                    escaping = True
                else:
                    buffer.append(c)

        return ''.join(buffer)

    def is_string(self):
        r = False
        str = ''
        startpos = self.pos

        if self.pos < len(self.expression) and self.expression[self.pos] in self.string_literal_quotes:
            quote_type = self.expression[self.pos]
            self.pos += 1

            while self.pos < len(self.expression):
                code = self.expression[self.pos]
                if code != quote_type or (str != '' and str[-1] == '\\'):
                    str += self.expression[self.pos]
                    self.pos += 1
                else:
                    self.pos += 1
                    self.tokennumber = self.unescape(str, startpos)
                    r = True
                    break
        return r

    def is_const(self):
        for i in self.consts:
            L = len(i)
            str = self.expression[self.pos:self.pos+L]
            if i == str:
                if len(self.expression) <= self.pos + L:
                    self.tokennumber = self.consts[i]
                    self.pos += L
                    return True
                if not self.expression[self.pos + L].isalnum() and self.expression[self.pos + L] != "_":
                    self.tokennumber = self.consts[i]
                    self.pos += L
                    return True
        return False

    def is_operator(self):
        ops = (
            ('**', 8, '**'),
            ('^', 8, '^'),
            ('%', 6, '%'),
            ('/', 6, '/'),
            (u'\u2219', 5, '*'), # bullet operator
            (u'\u2022', 5, '*'), # black small circle
            ('*', 5, '*'),
            ('+', 4, '+'),
            ('-', 4, '-'),
            ('||', 3, '||'),
            ('==', 3, '=='),
            ('!=', 3, '!='),
            ('<=', 3, '<='),
            ('>=', 3, '>='),
            ('<', 3, '<'),
            ('>', 3, '>'),
            ('in ', 3, 'in'),
            ('not ', 2, 'not'),
            ('and ', 1, 'and'),
            ('xor ', 0, 'xor'),
            ('or ', 0, 'or'),
        )

        for token, priority, index in ops:
            if self.expression.startswith(token, self.pos):
                self.tokenprio = priority
                self.tokenindex = index
                self.pos += len(token)
                return True

        return False

    def is_sign(self):
        code = self.expression[self.pos - 1]
        return (code == '+') or (code == '-')

    def is_positive_sign(self):
        code = self.expression[self.pos - 1]
        return code == '+'

    def is_negative_sign(self):
        code = self.expression[self.pos - 1]
        return code == '-'

    def is_logical_not(self):
        code = self.expression[self.pos - 4: self.pos]
        return code == 'not '

    def is_left_parenth(self):
        code = self.expression[self.pos]
        if code == '(':
            self.pos += 1
            self.tmpprio += 10
            return True

        return False

    def is_right_parenth(self):
        code = self.expression[self.pos]
        if code == ')':
            self.pos += 1
            self.tmpprio -= 10
            return True

        return False

    def is_comma(self):
        code = self.expression[self.pos]
        if code==',':
            self.pos+=1
            self.tokenprio=-1
            self.tokenindex=","
            return True

        return False

    def is_white(self):
        code = self.expression[self.pos]
        if code.isspace():
            self.pos += 1
            return True

        return False

    def is_unary_operator(self):
        str = ''

        for i in range(self.pos, len(self.expression)):
            c = self.expression[i]

            if c.upper() == c.lower():
                if i == self.pos or (c != '_' and (c < '0' or c > '9')):
                    break

            str += c

        if len(str) > 0 and str in self.ops1:
            self.tokenindex = str
            self.tokenprio = 9
            self.pos += len(str)
            return True

        return False

    def is_binary_operator(self):
        str = ''

        for i in range(self.pos, len(self.expression)):
            c = self.expression[i]
            if c.upper() == c.lower():
                if i == self.pos or (c != '_' and (c < '0' or c > '9')):
                    break
            str += c

        if len(str) > 0 and (str in self.ops2):
            self.tokenindex = str
            self.tokenprio = 9
            self.pos += len(str)

            return True

        return False

    def is_var(self):
        str = ''
        inQuotes = False

        for i in range(self.pos, len(self.expression)):
            c = self.expression[i]
            if c.lower() == c.upper():
                if ((i == self.pos and c != '"') or (not (c in '_."') and (c < '0' or c > '9'))) and not inQuotes :
                    break

            if c == '"':
                inQuotes = not inQuotes
            str += c

        if str:
            self.tokenindex = str
            self.tokenprio = 6
            self.pos += len(str)

            return True

        return False

    def is_comment(self):
        code = self.expression[self.pos - 1]

        if code == '/' and self.expression[self.pos] == '*':
            self.pos = self.expression.index('*/', self.pos) + 2

            if self.pos == 1:
                self.pos = len(self.expression)

            return True

        return False
