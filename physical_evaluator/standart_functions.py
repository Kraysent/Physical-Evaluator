import math
import random as rnd

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    return a / b

def pow(a, b):
    return a ** b

def min(a, b):
    return min(a, b)

def max(a, b):
    return max(a, b)

def log(x, b):
    return math.log(x, b)

def sqrt(a):
    return math.sqrt(a)

def exp(a):
    return math.exp(a)

def ceil(a):
    return math.ceil(a)

def floor(a):
    return math.floor(a)

def round(a):
    return round(a)

def abs(a):
    return abs(a)

def mod(a, b):
    return a % b

def concat(a, b,*args):
    result=u'{0}{1}'.format(a, b)
    for arg in args:
        result=u'{0}{1}'.format(result, arg)
    return result

def equal (a, b ):
    return a == b

def not_equal (a, b ):
    return a != b

def greater_than (a, b ):
    return a > b

def less_than (a, b ):
    return a < b

def greater_than_equal (a, b ):
    return a >= b

def less_than_equal (a, b ):
    return a <= b

def and_operator (a, b ):
    return ( a and b )

def or_operator (a, b ):
    return  ( a or  b )

def xor_operator (a, b ):
    return  ( a ^ b )

def in_operator(a, b):
    return a in b

def not_operator(a):
    return not a

def neg(a):
    return -a

def random(a):
    return rnd.random() * (a or 1)

def fac(a):  # a!
    return math.factorial(a)

def pyt(a, b):
    return math.sqrt(a * a + b * b)

def sin(a):
    return math.sin(a)

def sind(a):
    return math.sin(math.radians(a))

def cos(a):
    return math.cos(a)

def cosd(a):
    return math.cos(math.radians(a))

def tan(a):
    return math.tan(a)

def tand(a):
    return math.tan(math.radians(a))

def asin(a):
    return math.asin(a)

def asind(a):
    return math.degrees(math.asin(a))

def acos(a):
    return math.acos(a)

def acosd(a):
    return math.degrees(math.acos(a))

def atan(a):
    return math.atan(a)

def atan2(a):
    return math.atan2(a)

def atand(a):
    return math.degrees(math.atan(a))

def roll(a, b):
    rolls = []
    roll = 0
    for c in range(1, a):
        roll = rnd.randint(1, b)
        rolls.append(roll)
    return rolls

def if_function(a, b, c):
    return b if a else c

def append(a, b):
    if type(a) != list:
        return [a, b]
    a.append(b)
    return a

unary_functions = {
    'sin': sin,
    'cos': cos,
    'tan': tan,
    'asin': asin,
    'acos': acos,
    'atan': atan,
    'sind': sind,
    'cosd': cosd,
    'tand': tand,
    'asind': asind,
    'acosd': acosd,
    'atand': atand,
    'sqrt': sqrt,
    'abs': abs,
    'ceil': ceil,
    'floor': floor,
    'round': round,
    '-': neg,
    'not': not_operator,
    'exp': exp,
}

binary_functions = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': div,
    '%': mod,
    '^': pow,
    '**': pow,
    ',': append,
    '||': concat,
    "==": equal,
    "!=": not_equal,
    ">": greater_than,
    "<": less_than,
    ">=": greater_than_equal,
    "<=": less_than_equal,
    "and": and_operator,
    "or": or_operator,
    "xor": xor_operator,
    "in": in_operator,
    "D": roll
}

functions = {
    'random': random,
    'fac': fac,
    'log': log,
    'min': min,
    'max': max,
    'pyt': pyt,
    'pow': pow,
    'atan2': atan2,
    'concat': concat,
    'if': if_function
}

constants = {
    'E': math.e,
    'PI': math.pi,
}