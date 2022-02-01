from py_expression_eval import Parser

parser = Parser()

print(parser.parse('2 < sin(x)').evaluate({ 'x': 5 }))
