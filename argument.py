import argparse
from latex2sympy2 import latex2sympy
import sympy as sp

def parse():
    parser = argparse.ArgumentParser(
            prog='fun-estimator',
            description='A simple function estimator using Sugeno inferencing system.')

    parser.add_argument('function', help='function in LaTeX format')
    parser.add_argument('dx', type=float, help='half length of trimf')

    inp = parser.parse_args()

    return {"dx": inp.dx,
            "LaTeX": inp.function,
            "function": sp.lambdify(sp.symbols('x'), sp.sympify(latex2sympy(inp.function)), 'numpy')}


