from py_expression_eval import Parser
from amuse.lab import units
import numpy as np

parser = Parser()

print(parser.parse('3 * vx').evaluate({ 'vx': np.array([1, 2, 3]) | units.kg }))
