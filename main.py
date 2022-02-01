from py_expression_eval import Parser

parser = Parser()

print(parser.parse('2 * x').evaluate({'x': 5}))
